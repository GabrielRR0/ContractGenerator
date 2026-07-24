# schemas/contracts

Modelos Pydantic **compartidos** del dominio "contratos" (no especificos de una plantilla puntual — esos viven en `services/contracts/templates/*.py`).

## Archivos

- **`contract_schemas.py`**:
  - `FieldSpec`: forma de un campo de formulario (`name`, `label`, `placeholder`, `type`). Cada plantilla expone su lista de `FIELDS` con esta forma para que el frontend arme el formulario dinamicamente, sin tener los campos de cada tipo de contrato hardcodeados.
  - `TemplateInfo`: respuesta de `GET /api/contracts/templates` — incluye `icono` (badge del selector de tipo) y `campos: list[FieldSpec]`.
  - `StyleInfo`: respuesta de `GET /api/contracts/styles`.
  - `GenerateContractRequest`: body de `POST /api/contracts/generate` (`template_id`, `style_id`, `data: dict[str, str]`). `data` es un dict generico (no un modelo fijo como antes `NdaData`) porque cada una de las 4 plantillas tiene campos completamente distintos — la validacion especifica ocurre dentro de `build_content()` de cada plantilla, no aca.
  - `PreviewContractRequest`: body de `POST /api/contracts/preview` (`template_id`, `data: dict[str, str]`, sin `style_id` porque el texto no depende del estilo visual).

## Por que `data` es un dict generico y no un modelo por plantilla

Con una sola plantilla (NDA) tenia sentido tipar `data: NdaData` directamente. Con 4 plantillas de forma distinta, forzar un tipo fijo en este schema hubiera requerido una union de 4 modelos (`NdaData | PrestacionServiciosData | ...`) sin poder discriminar cual usar sin ya conocer `template_id` de antemano. Es mas simple y explicito validar dentro de cada `build_content()`, que ya sabe que plantilla es.
