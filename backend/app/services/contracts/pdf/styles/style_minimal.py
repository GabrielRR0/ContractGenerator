from fpdf import FPDF

STYLE_ID = "minimal"
STYLE_NOMBRE = {"es": "Minimalista", "en": "Minimal"}
STYLE_DESCRIPCION = {
    "es": "Tipografia limpia, sin adornos, margenes amplios.",
    "en": "Clean typography, no ornamentation, generous margins.",
}


def apply(pdf: FPDF, content: dict) -> None:
    # Dibuja el documento completo: titulo, parrafos y firmas, en ese orden.
    pdf.set_margins(25, 25, 25)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 12, content["titulo"], new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    pdf.set_font("Helvetica", "", 11)
    for parrafo in content["parrafos"]:
        pdf.multi_cell(0, 7, parrafo)
        pdf.ln(4)

    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)
    for firma in content["firmas"]:
        pdf.cell(0, 7, "_" * 30, new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 7, firma, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)
