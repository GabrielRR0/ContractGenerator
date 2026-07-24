from pydantic import BaseModel


class FieldSpec(BaseModel):
    """Describe un campo de formulario para que el frontend lo renderice dinamicamente."""

    name: str
    label: str
    placeholder: str = ""
    type: str = "text"  # "text" | "date" | "textarea"
    # Espeja el max_length del modelo Pydantic de la plantilla (ver
    # templates/*.py): el frontend lo usa para mostrar un contador en vivo y
    # bloquear el envio antes de pegarle al backend. None = sin limite
    # (ej. el campo "fecha").
    max_length: int | None = None


class TemplateInfo(BaseModel):
    id: str
    nombre: str
    descripcion: str
    icono: str
    campos: list[FieldSpec]


class StyleInfo(BaseModel):
    id: str
    nombre: str
    descripcion: str


class GenerateContractRequest(BaseModel):
    template_id: str
    style_id: str
    # dict generico (no un modelo fijo tipo NdaData): cada plantilla define y
    # valida su propia forma de datos en su modulo (ver templates/*.py), ya
    # que las 4 plantillas tienen campos completamente distintos entre si.
    data: dict[str, str]
    # Idioma del documento generado ("es" | "en"); ver templates/i18n.py.
    locale: str = "es"


class PreviewContractRequest(BaseModel):
    template_id: str
    data: dict[str, str]
    locale: str = "es"
    # Opcional: si viene, el preview tambien devuelve la cantidad real de
    # paginas que va a tener el PDF con ese estilo (ver contract_service.py).
    style_id: str | None = None
