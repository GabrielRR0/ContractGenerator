import pytest

from app.services.contracts.pdf.generator import STYLES, generate_pdf_bytes

CONTENT = {
    "titulo": "Acuerdo de Confidencialidad",
    "parrafos": ["Parrafo de prueba.", "Segundo parrafo de prueba."],
    "firmas": ["Parte A", "Parte B"],
}


@pytest.mark.parametrize("style_id", ["minimal", "classic", "corporate", "modern"])
def test_generate_pdf_bytes_con_cada_estilo(style_id: str):
    print(f"\n[test] Generando PDF de prueba con estilo '{style_id}'...")
    pdf_bytes = generate_pdf_bytes(style_id, CONTENT)

    assert pdf_bytes.startswith(b"%PDF-")
    print(f"[test] OK: estilo '{style_id}' genero un PDF valido ({len(pdf_bytes)} bytes).")


def test_styles_registrados_coinciden_con_los_4_esperados():
    assert set(STYLES.keys()) == {"minimal", "classic", "corporate", "modern"}


def test_generate_pdf_bytes_con_estilo_desconocido_lanza_error():
    with pytest.raises(ValueError):
        generate_pdf_bytes("estilo_inexistente", CONTENT)
