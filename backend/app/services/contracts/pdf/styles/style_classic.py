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
    for firma in content["firmas"]:
        pdf.cell(0, 7, "_" * 30, new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 7, firma, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)
