# services/contracts/templates

Cada archivo de esta carpeta representa **un tipo de documento** (una plantilla) y define exclusivamente su **contenido**: que texto va, en que orden, con que datos del formulario se rellena, y que campos pide ese formulario — en espanol e ingles por igual. No sabe nada de PDF ni de estilos visuales — eso es responsabilidad de `pdf/` (carpeta hermana en `services/contracts/`).

## Convencion de cada archivo de plantilla

Cada modulo expone:
- `TEMPLATE_ID`: identificador usado en la API (`template_id`) y en el diccionario `TEMPLATES` de `contract_service.py`.
- `TEMPLATE_NOMBRE` / `TEMPLATE_DESCRIPCION`: **dicts** `{"es": "...", "en": "..."}` (no strings sueltos) — metadata legible que se muestra en el selector de tipo del frontend, resuelta al locale pedido con `i18n.pick()`.
- `TEMPLATE_ICONO`: codigo corto (2-3 letras, ej. `"NDA"`, `"CL"`) para el badge visual — no se traduce, es el mismo en cualquier idioma.
- `FIELDS`: lista de dicts `{name, label, placeholder, type}`, donde `label` y `placeholder` son a su vez dicts `{"es": ..., "en": ...}`. El frontend nunca ve esta estructura cruda — `contract_service.list_templates(locale)` ya la resuelve antes de responder.
- Un modelo Pydantic privado del modulo (ej. `NdaData`) que valida los datos requeridos (los nombres de campo son iguales en los dos idiomas, solo cambia el texto mostrado al usuario).
- `build_content(data: dict, locale: str = "es") -> dict`: valida `data` contra ese modelo y devuelve el contenido final (`titulo`, `parrafos`, `firmas`) **en el idioma pedido** para generar el PDF real. Lanza `pydantic.ValidationError` si falta un campo (el service lo convierte en `ValueError` -> 422).
- `build_preview(data: dict, locale: str = "es") -> dict`: misma forma de salida, pero **sin validar** — rellena los campos faltantes con un placeholder entre corchetes (`[campo]`, usando el label ya traducido) via `placeholders.value_or_placeholder`. La usa `POST /api/contracts/preview` para el preview en vivo mientras el usuario todavia esta completando el formulario.

## Archivos

- **`i18n.py`**: `pick(texts, locale)` — helper minimo que resuelve un dict `{"es": ..., "en": ...}` al idioma pedido, con fallback a español si el locale no esta traducido para ese texto puntual.
- **`placeholders.py`**: helper compartido `value_or_placeholder(data, key, label)` usado por los 4 `build_preview` para no repetir el mismo `if`. Recibe el `label` ya traducido (no sabe de locales).
- **`standard_clauses.py`**: `standard_clauses(locale)` devuelve 3 parrafos de cierre comunes a cualquier contrato (vigencia, ley aplicable/jurisdiccion, notificaciones) en el idioma pedido — se agregan al final de `parrafos` en los 4 `build_content`/`build_preview` para que el documento generado se lea como un contrato completo y no como un resumen de 2-3 lineas.
- **`nda_template.py`**: Acuerdo de Confidencialidad / Non-Disclosure Agreement (partes, fecha, clausula de confidencialidad — campo grande).
- **`prestacion_servicios_template.py`**: Prestacion de Servicios / Service Agreement (contratante, proveedor, alcance del servicio — campo grande, monto, plazo).
- **`contrato_laboral_template.py`**: Contrato Laboral / Employment Contract (empleador, empleado, puesto, salario, jornada, clausulas adicionales — campo grande).
- **`contrato_arrendamiento_template.py`**: Contrato de Arrendamiento / Lease Agreement (arrendador, arrendatario, direccion, monto, duracion, clausulas adicionales — campo grande).

Las 4 plantillas tienen al menos un campo `type: "textarea"` para texto libre de varios parrafos — un contrato real necesita mas contenido que un dato suelto por linea, y ese campo (sumado a `standard_clauses.py`) es lo que le da cuerpo al documento generado, en cualquiera de los dos idiomas.

## Por que esta separacion

Cada plantilla es independiente y no conoce a las demas — agregar una plantilla nueva no implica tocar las existentes, solo crear el archivo (con `FIELDS`, `build_content` y `build_preview`, ambos bilingues) y registrarlo en `TEMPLATES` de `contract_service.py`. El frontend nunca necesita un `if template_id === ...` propio, ni tampoco un diccionario de traduccion propio para el contenido del documento: renderiza el formulario a partir de `FIELDS` y pide el idioma via `locale`, sin importar cuantas plantillas existan.
