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
    # Firmas lado a lado (izquierda/derecha), como en un contrato real, en vez
    # de apiladas: una linea real (no texto con guiones) por columna, ajustada
    # al ancho disponible entre margenes.
    firma_izq, firma_der = content["firmas"]
    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    gap = 20
    col_width = (page_width - gap) / 2
    left_x = pdf.l_margin
    right_x = pdf.l_margin + col_width + gap
    line_y = pdf.get_y() + 7
    pdf.line(left_x, line_y, left_x + col_width, line_y)
    pdf.line(right_x, line_y, right_x + col_width, line_y)
    pdf.set_xy(left_x, line_y)
    pdf.cell(col_width, 7, firma_izq)
    pdf.set_xy(right_x, line_y)
    pdf.cell(col_width, 7, firma_der, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
