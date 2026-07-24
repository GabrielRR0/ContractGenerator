from fpdf import FPDF

STYLE_ID = "modern"
STYLE_NOMBRE = {"es": "Moderno", "en": "Modern"}
STYLE_DESCRIPCION = {
    "es": "Acento de color y jerarquia tipografica contemporanea.",
    "en": "Color accent and contemporary typographic hierarchy.",
}

_ACCENT = (0, 113, 227)  # mismo azul de acento del frontend (ver DESIGN.md)


def apply(pdf: FPDF, content: dict) -> None:
    # Titulo grande con una linea de acento debajo (jerarquia tipografica
    # marcada), espaciado generoso entre bloques.
    pdf.set_margins(25, 25, 25)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*_ACCENT)
    pdf.cell(0, 12, content["titulo"], new_x="LMARGIN", new_y="NEXT")

    pdf.set_draw_color(*_ACCENT)
    pdf.set_line_width(1)
    pdf.line(pdf.l_margin, pdf.get_y() + 2, pdf.l_margin + 30, pdf.get_y() + 2)
    pdf.ln(12)

    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Helvetica", "", 11.5)
    for parrafo in content["parrafos"]:
        pdf.multi_cell(0, 8, parrafo)
        pdf.ln(5)

    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)
    # Firmas lado a lado (izquierda/derecha). set_line_width se resetea a un
    # trazo fino: el titulo dejo el grosor en 1 (linea de acento gruesa) y
    # fpdf2 mantiene ese estado si no se lo pisa.
    firma_izq, firma_der = content["firmas"]
    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    gap = 20
    col_width = (page_width - gap) / 2
    left_x = pdf.l_margin
    right_x = pdf.l_margin + col_width + gap
    line_y = pdf.get_y() + 7
    pdf.set_draw_color(*_ACCENT)
    pdf.set_line_width(0.2)
    pdf.line(left_x, line_y, left_x + col_width, line_y)
    pdf.line(right_x, line_y, right_x + col_width, line_y)
    pdf.set_text_color(30, 30, 30)
    pdf.set_xy(left_x, line_y)
    pdf.cell(col_width, 7, firma_izq)
    pdf.set_xy(right_x, line_y)
    pdf.cell(col_width, 7, firma_der, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
