from datetime import date

from pydantic import BaseModel, Field

from app.services.contracts.templates.i18n import pick
from app.services.contracts.templates.placeholders import value_or_placeholder
from app.services.contracts.templates.standard_clauses import standard_clauses

TEMPLATE_ID = "prestacion_servicios"
TEMPLATE_NOMBRE = {"es": "Prestacion de Servicios", "en": "Service Agreement"}
TEMPLATE_DESCRIPCION = {
    "es": "Define alcance, monto y plazo de un servicio profesional.",
    "en": "Defines the scope, fee, and term of a professional service.",
}
TEMPLATE_ICONO = "PS"

FIELDS = [
    {
        "name": "contratante",
        "label": {"es": "Contratante", "en": "Client"},
        "placeholder": {"es": "Ej. Empresa ABC S.A.", "en": "E.g. ABC Company Inc."},
        "type": "text",
    },
    {
        "name": "proveedor",
        "label": {"es": "Proveedor", "en": "Provider"},
        "placeholder": {"es": "Ej. Juan Perez", "en": "E.g. John Smith"},
        "type": "text",
    },
    {"name": "fecha", "label": {"es": "Fecha", "en": "Date"}, "placeholder": {"es": "", "en": ""}, "type": "date"},
    {
        "name": "alcance_servicio",
        "label": {"es": "Alcance del servicio", "en": "Service scope"},
        "placeholder": {
            "es": "Ej. Desarrollo de un sitio web institucional",
            "en": "E.g. Development of a corporate website",
        },
        "type": "textarea",
    },
    {
        "name": "monto",
        "label": {"es": "Monto", "en": "Fee"},
        "placeholder": {"es": "Ej. $500.000", "en": "E.g. $5,000"},
        "type": "text",
    },
    {
        "name": "plazo",
        "label": {"es": "Plazo", "en": "Term"},
        "placeholder": {"es": "Ej. 6 meses", "en": "E.g. 6 months"},
        "type": "text",
    },
]


class PrestacionServiciosData(BaseModel):
    contratante: str = Field(..., min_length=1, max_length=200)
    proveedor: str = Field(..., min_length=1, max_length=200)
    fecha: date
    alcance_servicio: str = Field(..., min_length=1, max_length=5000)
    monto: str = Field(..., min_length=1, max_length=200)
    plazo: str = Field(..., min_length=1, max_length=200)


def build_content(data: dict[str, str], locale: str = "es") -> dict:
    validated = PrestacionServiciosData(**data)
    if locale == "en":
        return {
            "titulo": "Service Agreement",
            "parrafos": [
                (
                    f'Between {validated.contratante} ("the Client") and {validated.proveedor} '
                    f'("the Provider"), dated {validated.fecha.isoformat()}.'
                ),
                f"Service scope: {validated.alcance_servicio}.",
                f"Fee: {validated.monto}. Term: {validated.plazo}.",
                *standard_clauses(locale),
            ],
            "firmas": [validated.contratante, validated.proveedor],
        }
    return {
        "titulo": "Contrato de Prestacion de Servicios",
        "parrafos": [
            (
                f'Entre {validated.contratante} ("el Contratante") y {validated.proveedor} '
                f'("el Proveedor"), con fecha {validated.fecha.isoformat()}.'
            ),
            f"Alcance del servicio: {validated.alcance_servicio}.",
            f"Monto: {validated.monto}. Plazo: {validated.plazo}.",
            *standard_clauses(locale),
        ],
        "firmas": [validated.contratante, validated.proveedor],
    }


def build_preview(data: dict[str, str], locale: str = "es") -> dict:
    campo_por_nombre = {campo["name"]: campo for campo in FIELDS}

    def valor(nombre: str) -> str:
        return value_or_placeholder(data, nombre, pick(campo_por_nombre[nombre]["label"], locale))

    contratante, proveedor, fecha = valor("contratante"), valor("proveedor"), valor("fecha")
    alcance, monto, plazo = valor("alcance_servicio"), valor("monto"), valor("plazo")

    if locale == "en":
        return {
            "titulo": "Service Agreement",
            "parrafos": [
                f'Between {contratante} ("the Client") and {proveedor} ("the Provider"), dated {fecha}.',
                f"Service scope: {alcance}.",
                f"Fee: {monto}. Term: {plazo}.",
                *standard_clauses(locale),
            ],
            "firmas": [contratante, proveedor],
        }
    return {
        "titulo": "Contrato de Prestacion de Servicios",
        "parrafos": [
            f'Entre {contratante} ("el Contratante") y {proveedor} ("el Proveedor"), con fecha {fecha}.',
            f"Alcance del servicio: {alcance}.",
            f"Monto: {monto}. Plazo: {plazo}.",
            *standard_clauses(locale),
        ],
        "firmas": [contratante, proveedor],
    }
