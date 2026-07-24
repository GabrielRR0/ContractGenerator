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
    for firma in content["firmas"]:
        pdf.set_draw_color(*_ACCENT)
        pdf.cell(0, 7, "_" * 30, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 7, firma, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)
