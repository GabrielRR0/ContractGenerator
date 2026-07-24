from fpdf import FPDF

STYLE_ID = "classic"
STYLE_NOMBRE = {"es": "Clasico", "en": "Classic"}
STYLE_DESCRIPCION = {
    "es": "Estilo formal con tipografia serif tradicional.",
    "en": "Formal style with traditional serif typography.",
}


def apply(pdf: FPDF, content: dict) -> None:
    # Titulo centrado en mayusculas + regla fina, cuerpo con sangria de
    # primera linea (convencion tipografica de documentos legales impresos).
    pdf.set_margins(28, 28, 28)
    pdf.add_page()

    pdf.set_font("Times", "B", 15)
    pdf.cell(0, 10, content["titulo"].upper(), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + page_width, pdf.get_y())
    pdf.ln(8)

    pdf.set_font("Times", "", 12)
    for parrafo in content["parrafos"]:
        pdf.cell(10)  # sangria de primera linea
        pdf.multi_cell(page_width - 10, 7, parrafo)
        pdf.ln(4)

    pdf.ln(10)
    pdf.set_font("Times", "I", 12)
    # Firmas lado a lado (izquierda/derecha); reutiliza page_width ya
    # calculado arriba para la regla del titulo.
    firma_izq, firma_der = content["firmas"]
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
