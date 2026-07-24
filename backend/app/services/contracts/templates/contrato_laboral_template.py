from datetime import date

from pydantic import BaseModel, Field

from app.services.contracts.templates.i18n import pick
from app.services.contracts.templates.placeholders import value_or_placeholder
from app.services.contracts.templates.standard_clauses import standard_clauses

TEMPLATE_ID = "contrato_laboral"
TEMPLATE_NOMBRE = {"es": "Contrato Laboral", "en": "Employment Contract"}
TEMPLATE_DESCRIPCION = {
    "es": "Formaliza la relacion entre empleador y empleado.",
    "en": "Formalizes the relationship between employer and employee.",
}
TEMPLATE_ICONO = "CL"

FIELDS = [
    {
        "name": "empleador",
        "label": {"es": "Empleador", "en": "Employer"},
        "placeholder": {"es": "Ej. Tech Solutions S.A.", "en": "E.g. Tech Solutions Inc."},
        "type": "text",
    },
    {
        "name": "empleado",
        "label": {"es": "Empleado", "en": "Employee"},
        "placeholder": {"es": "Ej. Maria Gonzalez", "en": "E.g. Mary Johnson"},
        "type": "text",
    },
    {
        "name": "fecha",
        "label": {"es": "Fecha de inicio", "en": "Start date"},
        "placeholder": {"es": "", "en": ""},
        "type": "date",
    },
    {
        "name": "puesto",
        "label": {"es": "Puesto", "en": "Position"},
        "placeholder": {"es": "Ej. Disenadora UX/UI", "en": "E.g. UX/UI Designer"},
        "type": "text",
    },
    {
        "name": "salario_mensual",
        "label": {"es": "Salario mensual", "en": "Monthly salary"},
        "placeholder": {"es": "Ej. $450.000", "en": "E.g. $4,500"},
        "type": "text",
    },
    {
        "name": "jornada_laboral",
        "label": {"es": "Jornada laboral", "en": "Work schedule"},
        "placeholder": {
            "es": "Ej. Tiempo completo, 40hs semanales",
            "en": "E.g. Full-time, 40 hours per week",
        },
        "type": "text",
    },
    {
        "name": "clausulas_adicionales",
        "label": {"es": "Clausulas adicionales", "en": "Additional clauses"},
        "placeholder": {
            "es": "Ej. periodo de prueba, beneficios, dias de vacaciones, condiciones de teletrabajo...",
            "en": "E.g. probationary period, benefits, vacation days, remote work conditions...",
        },
        "type": "textarea",
    },
]


class ContratoLaboralData(BaseModel):
    empleador: str = Field(..., min_length=1, max_length=200)
    empleado: str = Field(..., min_length=1, max_length=200)
    fecha: date
    puesto: str = Field(..., min_length=1, max_length=200)
    salario_mensual: str = Field(..., min_length=1, max_length=200)
    jornada_laboral: str = Field(..., min_length=1, max_length=200)
    clausulas_adicionales: str = Field(..., min_length=1, max_length=5000)


def build_content(data: dict[str, str], locale: str = "es") -> dict:
    validated = ContratoLaboralData(**data)
    if locale == "en":
        return {
            "titulo": "Employment Contract",
            "parrafos": [
                (
                    f'Between {validated.empleador} ("the Employer") and {validated.empleado} '
                    f'("the Employee"), with start date {validated.fecha.isoformat()}.'
                ),
                f"Position: {validated.puesto}. Schedule: {validated.jornada_laboral}.",
                f"Agreed monthly salary: {validated.salario_mensual}.",
                validated.clausulas_adicionales,
                *standard_clauses(locale),
            ],
            "firmas": [validated.empleador, validated.empleado],
        }
    return {
        "titulo": "Contrato de Trabajo",
        "parrafos": [
            (
                f'Entre {validated.empleador} ("el Empleador") y {validated.empleado} '
                f'("el Empleado"), con fecha de inicio {validated.fecha.isoformat()}.'
            ),
            f"Puesto: {validated.puesto}. Jornada: {validated.jornada_laboral}.",
            f"Salario mensual acordado: {validated.salario_mensual}.",
            validated.clausulas_adicionales,
            *standard_clauses(locale),
        ],
        "firmas": [validated.empleador, validated.empleado],
    }


def build_preview(data: dict[str, str], locale: str = "es") -> dict:
    campo_por_nombre = {campo["name"]: campo for campo in FIELDS}

    def valor(nombre: str) -> str:
        return value_or_placeholder(data, nombre, pick(campo_por_nombre[nombre]["label"], locale))

    empleador, empleado, fecha = valor("empleador"), valor("empleado"), valor("fecha")
    puesto, salario, jornada = valor("puesto"), valor("salario_mensual"), valor("jornada_laboral")
    clausulas_adicionales = valor("clausulas_adicionales")

    if locale == "en":
        return {
            "titulo": "Employment Contract",
            "parrafos": [
                f'Between {empleador} ("the Employer") and {empleado} ("the Employee"), with start date {fecha}.',
                f"Position: {puesto}. Schedule: {jornada}.",
                f"Agreed monthly salary: {salario}.",
                clausulas_adicionales,
                *standard_clauses(locale),
            ],
            "firmas": [empleador, empleado],
        }
    return {
        "titulo": "Contrato de Trabajo",
        "parrafos": [
            f'Entre {empleador} ("el Empleador") y {empleado} ("el Empleado"), con fecha de inicio {fecha}.',
            f"Puesto: {puesto}. Jornada: {jornada}.",
            f"Salario mensual acordado: {salario}.",
            clausulas_adicionales,
            *standard_clauses(locale),
        ],
        "firmas": [empleador, empleado],
    }
