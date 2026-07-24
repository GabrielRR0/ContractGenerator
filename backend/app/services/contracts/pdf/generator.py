from fpdf import FPDF

from app.services.contracts.pdf.styles import style_classic, style_corporate, style_minimal, style_modern

STYLES = {
    style_minimal.STYLE_ID: style_minimal,
    style_classic.STYLE_ID: style_classic,
    style_corporate.STYLE_ID: style_corporate,
    style_modern.STYLE_ID: style_modern,
}


def generate_pdf_bytes(style_id: str, content: dict) -> bytes:
    # El estilo decide todo el layout (pagina, fuentes, margenes); esta funcion
    # solo resuelve cual estilo aplicar y devuelve el binario final.
    style_module = STYLES.get(style_id)
    if style_module is None:
        raise ValueError(f"Estilo desconocido: {style_id}")

    pdf = FPDF()
    style_module.apply(pdf, content)
    return bytes(pdf.output())


def count_pages(style_id: str, content: dict) -> int:
    # Corre el mismo renderer real que generate_pdf_bytes (mismo apply()),
    # pero sin serializar a bytes: alcanza con leer pdf.page al terminar,
    # que fpdf2 incrementa en cada add_page() interno y al final del render
    # equivale al total de paginas reales (no es una estimacion).
    style_module = STYLES.get(style_id)
    if style_module is None:
        raise ValueError(f"Estilo desconocido: {style_id}")

    pdf = FPDF()
    style_module.apply(pdf, content)
    return pdf.page
