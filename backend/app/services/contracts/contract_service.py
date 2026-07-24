from pydantic import ValidationError

from app.schemas.contracts.contract_schemas import FieldSpec, GenerateContractRequest, StyleInfo, TemplateInfo
from app.services.contracts.pdf.generator import STYLES, count_pages, generate_pdf_bytes
from app.services.contracts.templates import (
    contrato_arrendamiento_template,
    contrato_laboral_template,
    nda_template,
    prestacion_servicios_template,
)
from app.services.contracts.templates.i18n import pick

TEMPLATES = {
    nda_template.TEMPLATE_ID: nda_template,
    prestacion_servicios_template.TEMPLATE_ID: prestacion_servicios_template,
    contrato_laboral_template.TEMPLATE_ID: contrato_laboral_template,
    contrato_arrendamiento_template.TEMPLATE_ID: contrato_arrendamiento_template,
}


def list_templates(locale: str = "es") -> list[TemplateInfo]:
    # Catalogo consumido por el frontend para armar el selector de plantillas
    # y renderizar el formulario dinamico segun los `campos` de cada una.
    # Ya viene traducido al locale pedido: el frontend no necesita saber nada
    # de i18n del lado del backend, solo pide el locale que quiere.
    return [
        TemplateInfo(
            id=mod.TEMPLATE_ID,
            nombre=pick(mod.TEMPLATE_NOMBRE, locale),
            descripcion=pick(mod.TEMPLATE_DESCRIPCION, locale),
            icono=mod.TEMPLATE_ICONO,
            campos=[
                FieldSpec(
                    name=campo["name"],
                    label=pick(campo["label"], locale),
                    placeholder=pick(campo["placeholder"], locale),
                    type=campo["type"],
                    max_length=campo.get("max_length"),
                )
                for campo in mod.FIELDS
            ],
        )
        for mod in TEMPLATES.values()
    ]


def list_styles(locale: str = "es") -> list[StyleInfo]:
    return [
        StyleInfo(id=mod.STYLE_ID, nombre=pick(mod.STYLE_NOMBRE, locale), descripcion=pick(mod.STYLE_DESCRIPCION, locale))
        for mod in STYLES.values()
    ]


def generate_document(request: GenerateContractRequest) -> bytes:
    # Orquestacion: la plantilla decide el texto (en el idioma pedido),
    # generate_pdf_bytes decide el estilo visual. Ninguna de las dos partes
    # conoce a la otra.
    template_module = TEMPLATES.get(request.template_id)
    if template_module is None:
        raise ValueError(f"Plantilla desconocida: {request.template_id}")

    try:
        content = template_module.build_content(request.data, request.locale)
    except ValidationError as exc:
        raise ValueError(f"Datos invalidos para la plantilla {request.template_id}: {exc}") from exc

    return generate_pdf_bytes(request.style_id, content)


def preview_document(template_id: str, data: dict[str, str], locale: str = "es", style_id: str | None = None) -> dict:
    # Version tolerante (sin validar campos requeridos) para el preview en
    # vivo del frontend mientras el usuario todavia esta completando el form.
    template_module = TEMPLATES.get(template_id)
    if template_module is None:
        raise ValueError(f"Plantilla desconocida: {template_id}")

    content = template_module.build_preview(data, locale)

    if style_id is not None:
        try:
            content["paginas"] = count_pages(style_id, content)
        except ValueError:
            # Estilo no reconocido (ej. catalogo todavia no cargo en el
            # frontend): el preview de texto sigue siendo valido, se omite
            # solo el conteo de paginas en vez de romper toda la respuesta.
            pass

    return content
