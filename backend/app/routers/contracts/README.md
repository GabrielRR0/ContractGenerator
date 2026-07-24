# routers/contracts

Capa HTTP del dominio "contratos". Traduce requests/responses REST hacia `services/contracts` — no contiene logica de negocio, solo validacion de entrada (via los schemas de Pydantic) y manejo de errores HTTP.

## Archivos

- **`contracts_router.py`**: define el `APIRouter` montado en `app/main.py` bajo el prefijo `/api/contracts`. Expone:
  - `GET /api/contracts/templates?locale=es|en` → lista las plantillas disponibles, ya traducidas al locale pedido (delega a `contract_service.list_templates`). `locale` es un query param opcional, default `"es"`.
  - `GET /api/contracts/styles?locale=es|en` → lista los estilos disponibles, idem.
  - `POST /api/contracts/preview` → recibe `{template_id, data, locale}` (sin `style_id`, el texto no depende del estilo) y devuelve el contenido JSON (`titulo`, `parrafos`, `firmas`) en el idioma pedido, tolerante a campos incompletos, para el preview en vivo del frontend mientras se completa el formulario.
  - `POST /api/contracts/generate` → recibe `{template_id, style_id, data, locale}`, genera el PDF via `contract_service.generate_document` (en el idioma pedido) y lo devuelve como binario (`application/pdf`) con `Content-Disposition: attachment`, no como JSON/base64, para que el navegador lo descargue directo. Si el service lanza `ValueError` (plantilla/estilo desconocido o datos invalidos), el router lo traduce a un `HTTPException(422)`.

  El backend hace toda la traduccion (ver `templates/i18n.py`) — el frontend solo pide el `locale` activo, nunca recibe textos sin traducir ni tiene que mapear nada del lado del cliente para el contenido del documento.

## Por que esta separacion

Mantener el router "delgado" (sin logica de PDF ni de plantillas) permite testear `contract_service` de forma aislada (sin HTTP) y reusarlo si en el futuro se agrega otro transporte (ej. un job programado que genere documentos).
