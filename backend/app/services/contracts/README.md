# services/contracts

Logica de negocio del generador de contratos. Es el punto de orquestacion entre "que plantilla eligio el usuario", "que estilo eligio" y "el renderizado final a PDF". El router HTTP (`routers/contracts/contracts_router.py`) es el unico consumidor de este modulo.

## Archivos

- **`contract_service.py`**: el orquestador. Expone cuatro funciones:
  - `list_templates()` / `list_styles()`: arman el catalogo (id, nombre, descripcion, icono, campos) que el frontend usa para el selector de tipo y el selector de estilo, leyendo la metadata de cada modulo registrado en `TEMPLATES` / `STYLES` (este ultimo importado de `pdf/generator.py`, no duplicado aca).
  - `generate_document(request)`: busca la plantilla por `template_id`, le pide su contenido validado (`build_content`) con los datos del formulario, y delega el renderizado a `pdf/generator.py` junto con el `style_id`. Lanza `ValueError` si la plantilla/estilo no existe o los datos son invalidos (el router lo convierte en HTTP 422).
  - `preview_document(template_id, data)`: version tolerante para el preview en vivo del frontend — usa `build_preview()` de la plantilla, que no exige campos completos.

## Subcarpetas

- **`templates/`**: una plantilla por tipo de documento (NDA, prestacion de servicios, contrato laboral, contrato de arrendamiento). Cada una define el contenido/texto y los campos de su formulario. Ver su propio README.
- **`pdf/`**: toma el contenido de una plantilla y lo renderiza a bytes de PDF aplicando un estilo (minimalista, clasico, corporativo, moderno). Ver su propio README.

## Por que se agrega una plantilla o estilo nuevo aca

Para soportar un nuevo tipo de documento: agregar un modulo en `templates/` con `FIELDS`, `build_content()` y `build_preview()`, y registrarlo en `TEMPLATES` de este archivo. Para un estilo visual nuevo: agregar un modulo en `pdf/styles/` con `apply()` y registrarlo en `STYLES` (`pdf/generator.py`) — `list_styles()` lo toma de ahi automaticamente. No hace falta tocar el router ni los schemas para agregar combinaciones nuevas.
