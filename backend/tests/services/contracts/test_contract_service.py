from pathlib import Path

import pytest

from app.schemas.contracts.contract_schemas import GenerateContractRequest
from app.services.contracts.contract_service import generate_document, list_styles, list_templates, preview_document

# Los PDFs generados durante los tests quedan aca para poder abrirlos y
# revisarlos a simple vista (no se versiona, ver .gitignore).
OUTPUT_DIR = Path(__file__).parent / "output"


def _nda_request(style_id: str = "minimal") -> GenerateContractRequest:
    return GenerateContractRequest(
        template_id="nda",
        style_id=style_id,
        data={
            "parte_reveladora": "Acme S.A.",
            "parte_receptora": "Juan Perez",
            "fecha": "2026-07-22",
            "clausula_confidencialidad": "La informacion no podra ser divulgada a terceros.",
        },
    )


def test_generate_document_devuelve_pdf_valido():
    print("\n[test] Generando NDA con estilo minimal...")
    pdf_bytes = generate_document(_nda_request())

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    assert pdf_bytes.startswith(b"%PDF-")

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / "nda_minimal.pdf"
    output_path.write_bytes(pdf_bytes)
    print(f"[test] OK: PDF valido ({len(pdf_bytes)} bytes). Guardado en {output_path}")


def test_generate_document_con_plantilla_desconocida_lanza_error():
    print("\n[test] Probando template_id inexistente, se espera ValueError...")
    request = _nda_request()
    request.template_id = "plantilla_inexistente"

    with pytest.raises(ValueError):
        generate_document(request)
    print("[test] OK: ValueError lanzado como se esperaba.")


def test_generate_document_con_campo_faltante_lanza_error():
    print("\n[test] Probando NDA sin 'parte_receptora', se espera ValueError...")
    request = _nda_request()
    del request.data["parte_receptora"]

    with pytest.raises(ValueError):
        generate_document(request)
    print("[test] OK: ValueError lanzado como se esperaba (dato requerido faltante).")


@pytest.mark.parametrize("template_id", ["nda", "prestacion_servicios", "contrato_laboral", "contrato_arrendamiento"])
@pytest.mark.parametrize("style_id", ["minimal", "classic", "corporate", "modern"])
def test_generate_document_todas_las_combinaciones(template_id: str, style_id: str):
    # Cubre las 16 combinaciones (4 plantillas x 4 estilos) con datos de
    # ejemplo minimos por plantilla, para detectar errores de renderizado
    # especificos de alguna combinacion puntual (ej. un estilo que rompe con
    # cierto contenido largo).
    datos_por_plantilla = {
        "nda": {
            "parte_reveladora": "Acme S.A.",
            "parte_receptora": "Juan Perez",
            "fecha": "2026-07-22",
            "clausula_confidencialidad": "No divulgar a terceros.",
        },
        "prestacion_servicios": {
            "contratante": "Empresa ABC S.A.",
            "proveedor": "Juan Perez",
            "fecha": "2026-07-22",
            "alcance_servicio": "Desarrollo de un sitio web institucional.",
            "monto": "$500.000",
            "plazo": "6 meses",
        },
        "contrato_laboral": {
            "empleador": "Tech Solutions S.A.",
            "empleado": "Maria Gonzalez",
            "fecha": "2026-07-22",
            "puesto": "Disenadora UX/UI",
            "salario_mensual": "$450.000",
            "jornada_laboral": "Tiempo completo, 40hs semanales",
            "clausulas_adicionales": "Periodo de prueba de 3 meses.",
        },
        "contrato_arrendamiento": {
            "arrendador": "Inmobiliaria Norte S.A.",
            "arrendatario": "Carlos Ramirez",
            "fecha": "2026-07-22",
            "direccion_inmueble": "Av. Libertador 1234, CABA",
            "monto_alquiler": "$180.000 mensuales",
            "duracion_contrato": "24 meses",
            "clausulas_adicionales": "No se permiten mascotas.",
        },
    }

    print(f"\n[test] Generando {template_id} con estilo {style_id}...")
    request = GenerateContractRequest(template_id=template_id, style_id=style_id, data=datos_por_plantilla[template_id])
    pdf_bytes = generate_document(request)

    assert pdf_bytes.startswith(b"%PDF-")
    print(f"[test] OK: {template_id} + {style_id} -> PDF valido ({len(pdf_bytes)} bytes).")


def test_list_templates_incluye_las_4_plantillas():
    print("\n[test] Verificando list_templates()...")
    ids = [t.id for t in list_templates()]
    assert set(ids) == {"nda", "prestacion_servicios", "contrato_laboral", "contrato_arrendamiento"}
    print(f"[test] OK: plantillas encontradas: {ids}")


def test_list_styles_incluye_los_4_estilos():
    print("\n[test] Verificando list_styles()...")
    ids = [s.id for s in list_styles()]
    assert set(ids) == {"minimal", "classic", "corporate", "modern"}
    print(f"[test] OK: estilos encontrados: {ids}")


def test_preview_document_con_datos_incompletos_no_lanza_error():
    print("\n[test] Probando preview_document con datos parciales (NDA)...")
    content = preview_document("nda", {"parte_reveladora": "Acme S.A."})

    assert "parte reveladora" not in content["parrafos"][0]  # el que si vino, no es placeholder
    assert "[parte receptora]" in content["parrafos"][0]
    print(f"[test] OK: preview con placeholders para campos faltantes: {content['parrafos'][0]}")


def test_list_templates_en_ingles_devuelve_nombres_traducidos():
    print("\n[test] Verificando list_templates(locale='en')...")
    templates_en = {t.id: t for t in list_templates("en")}
    assert templates_en["nda"].nombre == "Non-Disclosure Agreement"
    assert templates_en["contrato_laboral"].nombre == "Employment Contract"
    campo_puesto = next(c for c in templates_en["contrato_laboral"].campos if c.name == "puesto")
    assert campo_puesto.label == "Position"
    print(f"[test] OK: nombres en ingles correctos, campo 'puesto' -> label '{campo_puesto.label}'")


def test_list_styles_en_ingles_devuelve_nombres_traducidos():
    print("\n[test] Verificando list_styles(locale='en')...")
    styles_en = {s.id: s for s in list_styles("en")}
    assert styles_en["minimal"].nombre == "Minimal"
    assert styles_en["corporate"].nombre == "Corporate"
    print("[test] OK: nombres de estilo en ingles correctos.")


def test_generate_document_en_ingles_devuelve_pdf_con_texto_en_ingles():
    print("\n[test] Generando NDA en ingles...")
    request = GenerateContractRequest(
        template_id="nda",
        style_id="minimal",
        locale="en",
        data={
            "parte_reveladora": "Acme Inc.",
            "parte_receptora": "John Smith",
            "fecha": "2026-07-22",
            "clausula_confidencialidad": "Information shall not be disclosed to third parties.",
        },
    )
    pdf_bytes = generate_document(request)

    assert pdf_bytes.startswith(b"%PDF-")
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / "nda_minimal_en.pdf"
    output_path.write_bytes(pdf_bytes)
    print(f"[test] OK: PDF en ingles valido ({len(pdf_bytes)} bytes). Guardado en {output_path}")


def test_preview_document_en_ingles_usa_placeholders_en_ingles():
    print("\n[test] Probando preview_document en ingles con datos parciales...")
    content = preview_document("nda", {"parte_reveladora": "Acme Inc."}, locale="en")

    assert content["titulo"] == "Non-Disclosure Agreement"
    assert "[receiving party]" in content["parrafos"][0]
    print(f"[test] OK: preview en ingles con placeholders correctos: {content['parrafos'][0]}")
