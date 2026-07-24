from fpdf import FPDF

STYLE_ID = "corporate"
STYLE_NOMBRE = {"es": "Corporativo", "en": "Corporate"}
STYLE_DESCRIPCION = {
    "es": "Encabezado marcado, estructura firme y profesional.",
    "en": "Bold header, firm and professional structure.",
}

_HEADER_FILL = (31, 41, 55)  # gris azulado oscuro
_HEADER_TEXT = (255, 255, 255)


def apply(pdf: FPDF, content: dict) -> None:
    # Barra de color solida detras del titulo (identidad corporativa), cuerpo
    # en bloques con mayor peso visual entre parrafos.
    pdf.set_margins(20, 0, 20)
    pdf.add_page()

    pdf.set_fill_color(*_HEADER_FILL)
    pdf.rect(0, 0, pdf.w, 30, style="F")
    pdf.set_xy(20, 10)
    pdf.set_text_color(*_HEADER_TEXT)
    pdf.set_font("Helvetica", "B", 17)
    pdf.cell(0, 12, content["titulo"], new_x="LMARGIN", new_y="NEXT")

    pdf.set_text_color(0, 0, 0)
    pdf.set_y(42)
    pdf.set_font("Helvetica", "", 11)
    for parrafo in content["parrafos"]:
        pdf.multi_cell(0, 7.5, parrafo)
        pdf.ln(5)

    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 11)
    for firma in content["firmas"]:
        pdf.cell(0, 7, "_" * 30, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 7, firma, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "B", 11)
        pdf.ln(6)
