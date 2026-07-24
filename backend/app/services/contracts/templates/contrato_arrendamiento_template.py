from datetime import date

from pydantic import BaseModel, Field

from app.services.contracts.templates.i18n import pick
from app.services.contracts.templates.placeholders import value_or_placeholder
from app.services.contracts.templates.standard_clauses import standard_clauses

TEMPLATE_ID = "contrato_arrendamiento"
TEMPLATE_NOMBRE = {"es": "Contrato de Arrendamiento", "en": "Lease Agreement"}
TEMPLATE_DESCRIPCION = {
    "es": "Establece los terminos de alquiler de un inmueble.",
    "en": "Establishes the terms for renting a property.",
}
TEMPLATE_ICONO = "AR"

FIELDS = [
    {
        "name": "arrendador",
        "label": {"es": "Arrendador", "en": "Landlord"},
        "placeholder": {"es": "Ej. Inmobiliaria Norte S.A.", "en": "E.g. Northgate Realty Inc."},
        "type": "text",
        "max_length": 200,
    },
    {
        "name": "arrendatario",
        "label": {"es": "Arrendatario", "en": "Tenant"},
        "placeholder": {"es": "Ej. Carlos Ramirez", "en": "E.g. Charles Miller"},
        "type": "text",
        "max_length": 200,
    },
    {
        "name": "fecha",
        "label": {"es": "Fecha de inicio", "en": "Start date"},
        "placeholder": {"es": "", "en": ""},
        "type": "date",
    },
    {
        "name": "direccion_inmueble",
        "label": {"es": "Direccion del inmueble", "en": "Property address"},
        "placeholder": {"es": "Ej. Av. Libertador 1234, CABA", "en": "E.g. 1234 Main St, Springfield"},
        "type": "text",
        "max_length": 200,
    },
    {
        "name": "monto_alquiler",
        "label": {"es": "Monto del alquiler", "en": "Rent amount"},
        "placeholder": {"es": "Ej. $180.000 mensuales", "en": "E.g. $1,800 per month"},
        "type": "text",
        "max_length": 200,
    },
    {
        "name": "duracion_contrato",
        "label": {"es": "Duracion del contrato", "en": "Contract duration"},
        "placeholder": {"es": "Ej. 24 meses", "en": "E.g. 24 months"},
        "type": "text",
        "max_length": 200,
    },
    {
        "name": "clausulas_adicionales",
        "label": {"es": "Clausulas adicionales", "en": "Additional clauses"},
        "placeholder": {
            "es": "Ej. condiciones de uso, mascotas, mantenimiento, deposito de garantia...",
            "en": "E.g. use conditions, pets, maintenance, security deposit...",
        },
        "type": "textarea",
        "max_length": 20000,
    },
]


class ContratoArrendamientoData(BaseModel):
    arrendador: str = Field(..., min_length=1, max_length=200)
    arrendatario: str = Field(..., min_length=1, max_length=200)
    fecha: date
    direccion_inmueble: str = Field(..., min_length=1, max_length=200)
    monto_alquiler: str = Field(..., min_length=1, max_length=200)
    duracion_contrato: str = Field(..., min_length=1, max_length=200)
    clausulas_adicionales: str = Field(..., min_length=1, max_length=20000)


def build_content(data: dict[str, str], locale: str = "es") -> dict:
    validated = ContratoArrendamientoData(**data)
    if locale == "en":
        return {
            "titulo": "Lease Agreement",
            "parrafos": [
                (
                    f'Between {validated.arrendador} ("the Landlord") and {validated.arrendatario} '
                    f'("the Tenant"), with start date {validated.fecha.isoformat()}.'
                ),
                f"Property located at: {validated.direccion_inmueble}.",
                f"Rent amount: {validated.monto_alquiler}. Duration: {validated.duracion_contrato}.",
                validated.clausulas_adicionales,
                *standard_clauses(locale),
            ],
            "firmas": [validated.arrendador, validated.arrendatario],
        }
    return {
        "titulo": "Contrato de Arrendamiento",
        "parrafos": [
            (
                f'Entre {validated.arrendador} ("el Arrendador") y {validated.arrendatario} '
                f'("el Arrendatario"), con fecha de inicio {validated.fecha.isoformat()}.'
            ),
            f"Inmueble ubicado en: {validated.direccion_inmueble}.",
            f"Monto del alquiler: {validated.monto_alquiler}. Duracion: {validated.duracion_contrato}.",
            validated.clausulas_adicionales,
            *standard_clauses(locale),
        ],
        "firmas": [validated.arrendador, validated.arrendatario],
    }


def build_preview(data: dict[str, str], locale: str = "es") -> dict:
    campo_por_nombre = {campo["name"]: campo for campo in FIELDS}

    def valor(nombre: str) -> str:
        return value_or_placeholder(data, nombre, pick(campo_por_nombre[nombre]["label"], locale))

    arrendador, arrendatario, fecha = valor("arrendador"), valor("arrendatario"), valor("fecha")
    direccion, monto, duracion = valor("direccion_inmueble"), valor("monto_alquiler"), valor("duracion_contrato")
    clausulas_adicionales = valor("clausulas_adicionales")

    if locale == "en":
        return {
            "titulo": "Lease Agreement",
            "parrafos": [
                (
                    f'Between {arrendador} ("the Landlord") and {arrendatario} ("the Tenant"), '
                    f"with start date {fecha}."
                ),
                f"Property located at: {direccion}.",
                f"Rent amount: {monto}. Duration: {duracion}.",
                clausulas_adicionales,
                *standard_clauses(locale),
            ],
            "firmas": [arrendador, arrendatario],
        }
    return {
        "titulo": "Contrato de Arrendamiento",
        "parrafos": [
            (
                f'Entre {arrendador} ("el Arrendador") y {arrendatario} ("el Arrendatario"), '
                f"con fecha de inicio {fecha}."
            ),
            f"Inmueble ubicado en: {direccion}.",
            f"Monto del alquiler: {monto}. Duracion: {duracion}.",
            clausulas_adicionales,
            *standard_clauses(locale),
        ],
        "firmas": [arrendador, arrendatario],
    }
