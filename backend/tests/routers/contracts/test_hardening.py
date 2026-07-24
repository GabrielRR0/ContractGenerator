from fastapi.testclient import TestClient

from app.config import settings
from app.main import app

client = TestClient(app)

VALID_NDA_PAYLOAD = {
    "template_id": "nda",
    "style_id": "minimal",
    "data": {
        "parte_reveladora": "Acme S.A.",
        "parte_receptora": "Juan Perez",
        "fecha": "2026-07-22",
        "clausula_confidencialidad": "La informacion no podra ser divulgada.",
    },
}


def test_post_generate_respeta_rate_limit_y_devuelve_429():
    print(f"\n[test] POST /api/contracts/generate mas alla de RATE_LIMIT_GENERATE ({settings.rate_limit_generate})...")
    limit = int(settings.rate_limit_generate.split("/")[0])

    for i in range(limit):
        response = client.post("/api/contracts/generate", json=VALID_NDA_PAYLOAD)
        assert response.status_code == 200, f"request {i + 1} deberia pasar bajo el limite"

    response = client.post("/api/contracts/generate", json=VALID_NDA_PAYLOAD)
    assert response.status_code == 429
    print(f"[test] OK: request {limit + 1} devolvio 429 como se esperaba.")


def test_post_generate_con_body_gigante_responde_413():
    print("\n[test] POST /api/contracts/generate con body > MAX_BODY_BYTES...")
    payload = {
        "template_id": "nda",
        "style_id": "minimal",
        "data": {
            "parte_reveladora": "Acme S.A.",
            "parte_receptora": "Juan Perez",
            "fecha": "2026-07-22",
            "clausula_confidencialidad": "a" * (settings.max_body_bytes + 5000),
        },
    }

    response = client.post("/api/contracts/generate", json=payload)

    assert response.status_code == 413
    print("[test] OK: status 413 como se esperaba.")


def test_post_generate_con_campo_demasiado_largo_responde_422():
    print("\n[test] POST /api/contracts/generate con clausula > max_length del campo (pero < MAX_BODY_BYTES)...")
    payload = {
        "template_id": "nda",
        "style_id": "minimal",
        "data": {
            "parte_reveladora": "Acme S.A.",
            "parte_receptora": "Juan Perez",
            "fecha": "2026-07-22",
            "clausula_confidencialidad": "a" * 5001,
        },
    }
    assert len(str(payload)) < settings.max_body_bytes, "el payload debe quedar por debajo del limite global de body"

    response = client.post("/api/contracts/generate", json=payload)

    assert response.status_code == 422
    print("[test] OK: status 422 como se esperaba.")


def test_get_templates_incluye_headers_de_seguridad():
    print("\n[test] GET /api/contracts/templates trae headers de seguridad...")
    response = client.get("/api/contracts/templates")

    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    print("[test] OK: headers de seguridad presentes.")
