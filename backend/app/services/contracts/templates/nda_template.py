from datetime import date

from pydantic import BaseModel, Field

from app.services.contracts.templates.i18n import pick
from app.services.contracts.templates.placeholders import value_or_placeholder
from app.services.contracts.templates.standard_clauses import standard_clauses

TEMPLATE_ID = "nda"
TEMPLATE_NOMBRE = {"es": "Acuerdo de Confidencialidad", "en": "Non-Disclosure Agreement"}
TEMPLATE_DESCRIPCION = {
    "es": "Protege informacion confidencial compartida entre las partes.",
    "en": "Protects confidential information shared between the parties.",
}
TEMPLATE_ICONO = "NDA"

FIELDS = [
    {
        "name": "parte_reveladora",
        "label": {"es": "Parte reveladora", "en": "Disclosing party"},
        "placeholder": {"es": "Ej. Acme S.A.", "en": "E.g. Acme Inc."},
        "type": "text",
    },
    {
        "name": "parte_receptora",
        "label": {"es": "Parte receptora", "en": "Receiving party"},
        "placeholder": {"es": "Ej. Juan Perez", "en": "E.g. John Smith"},
        "type": "text",
    },
    {"name": "fecha", "label": {"es": "Fecha", "en": "Date"}, "placeholder": {"es": "", "en": ""}, "type": "date"},
    {
        "name": "clausula_confidencialidad",
        "label": {"es": "Clausula de confidencialidad", "en": "Confidentiality clause"},
        "placeholder": {
            "es": "Detalle el alcance de la confidencialidad...",
            "en": "Describe the scope of confidentiality...",
        },
        "type": "textarea",
    },
]


class NdaData(BaseModel):
    parte_reveladora: str = Field(..., min_length=1, max_length=200)
    parte_receptora: str = Field(..., min_length=1, max_length=200)
    fecha: date
    clausula_confidencialidad: str = Field(..., min_length=1, max_length=5000)


def build_content(data: dict[str, str], locale: str = "es") -> dict:
    """Contenido final (datos validados) para generar el PDF real."""
    validated = NdaData(**data)
    if locale == "en":
        return {
            "titulo": "Non-Disclosure Agreement",
            "parrafos": [
                (
                    f"Between {validated.parte_reveladora} and {validated.parte_receptora}, "
                    f"dated {validated.fecha.isoformat()}."
                ),
                validated.clausula_confidencialidad,
                *standard_clauses(locale),
            ],
            "firmas": [validated.parte_reveladora, validated.parte_receptora],
        }
    return {
        "titulo": "Acuerdo de Confidencialidad",
        "parrafos": [
            (
                f"Entre {validated.parte_reveladora} y {validated.parte_receptora}, "
                f"con fecha {validated.fecha.isoformat()}."
            ),
            validated.clausula_confidencialidad,
            *standard_clauses(locale),
        ],
        "firmas": [validated.parte_reveladora, validated.parte_receptora],
    }


def build_preview(data: dict[str, str], locale: str = "es") -> dict:
    """Version tolerante (sin validar) para el preview en vivo, con datos incompletos."""
    campo_por_nombre = {campo["name"]: campo for campo in FIELDS}
    parte_reveladora = value_or_placeholder(data, "parte_reveladora", pick(campo_por_nombre["parte_reveladora"]["label"], locale))
    parte_receptora = value_or_placeholder(data, "parte_receptora", pick(campo_por_nombre["parte_receptora"]["label"], locale))
    fecha = value_or_placeholder(data, "fecha", pick(campo_por_nombre["fecha"]["label"], locale))
    clausula = value_or_placeholder(
        data, "clausula_confidencialidad", pick(campo_por_nombre["clausula_confidencialidad"]["label"], locale)
    )

    if locale == "en":
        return {
            "titulo": "Non-Disclosure Agreement",
            "parrafos": [f"Between {parte_reveladora} and {parte_receptora}, dated {fecha}.", clausula, *standard_clauses(locale)],
            "firmas": [parte_reveladora, parte_receptora],
        }
    return {
        "titulo": "Acuerdo de Confidencialidad",
        "parrafos": [f"Entre {parte_reveladora} y {parte_receptora}, con fecha {fecha}.", clausula, *standard_clauses(locale)],
        "firmas": [parte_reveladora, parte_receptora],
    }
