_CLAUSES_ES = [
    (
        "Vigencia: el presente contrato entra en vigencia en la fecha indicada y se "
        "mantiene vigente hasta el cumplimiento total de las obligaciones aqui asumidas, "
        "salvo rescision anticipada notificada por escrito con al menos 15 dias de anticipacion."
    ),
    (
        "Ley aplicable y jurisdiccion: este contrato se rige por las leyes vigentes en el "
        "domicilio de las partes, sometiendose a sus tribunales competentes ante cualquier "
        "controversia derivada de su interpretacion o cumplimiento."
    ),
    (
        "Notificaciones: toda comunicacion relacionada con este contrato debera realizarse "
        "por escrito a los domicilios o medios de contacto declarados por cada parte, "
        "surtiendo efecto a partir de su recepcion."
    ),
]

_CLAUSES_EN = [
    (
        "Term: this agreement takes effect on the date indicated and remains in force "
        "until all obligations set out herein have been fully performed, unless terminated "
        "early upon at least 15 days' written notice."
    ),
    (
        "Governing law and jurisdiction: this agreement is governed by the laws applicable "
        "at the parties' domicile, and any dispute arising from its interpretation or "
        "performance shall be submitted to the competent courts thereof."
    ),
    (
        "Notices: any communication related to this agreement must be made in writing to "
        "the addresses or contact details provided by each party, and shall take effect "
        "upon receipt."
    ),
]


def standard_clauses(locale: str = "es") -> list[str]:
    """Clausulas de cierre comunes a cualquier contrato (no dependen de datos
    del formulario), para que el documento generado se lea como un contrato
    real completo y no solo como un resumen de 2-3 lineas."""
    return _CLAUSES_EN if locale == "en" else _CLAUSES_ES
