from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Los PDFs generados durante los tests quedan aca para poder abrirlos y
# revisarlos a simple vista (no se versiona, ver .gitignore).
OUTPUT_DIR = Path(__file__).parent / "output"


def test_get_templates_incluye_las_4_plantillas():
    print("\n[test] GET /api/contracts/templates...")
    response = client.get("/api/contracts/templates")

    assert response.status_code == 200
    body = response.json()
    ids = [t["id"] for t in body]
    assert set(ids) == {"nda", "prestacion_servicios", "contrato_laboral", "contrato_arrendamiento"}
    # Cada plantilla debe traer sus campos para que el frontend arme el form.
    assert all("campos" in t and len(t["campos"]) > 0 for t in body)
    print(f"[test] OK: status 200, plantillas: {ids}")


def test_get_styles_incluye_los_4_estilos():
    print("\n[test] GET /api/contracts/styles...")
    response = client.get("/api/contracts/styles")

    assert response.status_code == 200
    ids = [s["id"] for s in response.json()]
    assert set(ids) == {"minimal", "classic", "corporate", "modern"}
    print(f"[test] OK: status 200, estilos: {ids}")


def test_post_preview_con_datos_incompletos_devuelve_placeholders():
    print("\n[test] POST /api/contracts/preview con datos parciales...")
    payload = {"template_id": "nda", "data": {"parte_reveladora": "Acme S.A."}}

    response = client.post("/api/contracts/preview", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "[parte receptora]" in body["parrafos"][0]
    print(f"[test] OK: status 200, preview: {body['parrafos'][0]}")


def test_post_generate_devuelve_pdf():
    print("\n[test] POST /api/contracts/generate con NDA + estilo minimal...")
    payload = {
        "template_id": "nda",
        "style_id": "minimal",
        "data": {
            "parte_reveladora": "Acme S.A.",
            "parte_receptora": "Juan Perez",
            "fecha": "2026-07-22",
            "clausula_confidencialidad": "La informacion no podra ser divulgada.",
        },
    }

    response = client.post("/api/contracts/generate", json=payload)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF-")

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / "nda_minimal_via_api.pdf"
    output_path.write_bytes(response.content)
    print(f"[test] OK: status 200, PDF valido ({len(response.content)} bytes). Guardado en {output_path}")


def test_post_generate_con_plantilla_nueva_devuelve_pdf():
    print("\n[test] POST /api/contracts/generate con Contrato Laboral + estilo corporate...")
    payload = {
        "template_id": "contrato_laboral",
        "style_id": "corporate",
        "data": {
            "empleador": "Tech Solutions S.A.",
            "empleado": "Maria Gonzalez",
            "fecha": "2026-07-22",
            "puesto": "Disenadora UX/UI",
            "salario_mensual": "$450.000",
            "jornada_laboral": "Tiempo completo, 40hs semanales",
            "clausulas_adicionales": "Periodo de prueba de 3 meses.",
        },
    }

    response = client.post("/api/contracts/generate", json=payload)

    assert response.status_code == 200
    assert response.content.startswith(b"%PDF-")

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / "contrato_laboral_corporate_via_api.pdf"
    output_path.write_bytes(response.content)
    print(f"[test] OK: status 200, PDF valido ({len(response.content)} bytes). Guardado en {output_path}")


def test_get_templates_con_locale_en_devuelve_nombres_en_ingles():
    print("\n[test] GET /api/contracts/templates?locale=en...")
    response = client.get("/api/contracts/templates?locale=en")

    assert response.status_code == 200
    nombres = {t["id"]: t["nombre"] for t in response.json()}
    assert nombres["nda"] == "Non-Disclosure Agreement"
    assert nombres["contrato_arrendamiento"] == "Lease Agreement"
    print(f"[test] OK: nombres en ingles: {nombres}")


def test_post_generate_con_locale_en_devuelve_pdf():
    print("\n[test] POST /api/contracts/generate con locale=en...")
    payload = {
        "template_id": "nda",
        "style_id": "modern",
        "locale": "en",
        "data": {
            "parte_reveladora": "Acme Inc.",
            "parte_receptora": "John Smith",
            "fecha": "2026-07-22",
            "clausula_confidencialidad": "Information shall not be disclosed to third parties.",
        },
    }

    response = client.post("/api/contracts/generate", json=payload)

    assert response.status_code == 200
    assert response.content.startswith(b"%PDF-")

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / "nda_modern_en_via_api.pdf"
    output_path.write_bytes(response.content)
    print(f"[test] OK: status 200, PDF en ingles valido ({len(response.content)} bytes). Guardado en {output_path}")


def test_post_generate_con_campo_faltante_responde_422():
    print("\n[test] POST /api/contracts/generate sin 'parte_receptora', se espera 422...")
    payload = {
        "template_id": "nda",
        "style_id": "minimal",
        "data": {
            "parte_reveladora": "Acme S.A.",
            "fecha": "2026-07-22",
            "clausula_confidencialidad": "texto",
        },
    }

    response = client.post("/api/contracts/generate", json=payload)

    assert response.status_code == 422
    print("[test] OK: status 422 como se esperaba.")
