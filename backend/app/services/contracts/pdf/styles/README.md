# services/contracts/pdf/styles

Cada archivo define **como se ve** el documento (tipografia, margenes, espaciado, disposicion de firmas) para un mismo contenido. No sabe nada del texto en si — recibe el `dict` de contenido ya armado por la plantilla (`templates/*.py`) y solo decide su presentacion visual.

## Convencion de cada archivo de estilo

Cada modulo expone:
- `STYLE_ID`: identificador usado en la API (`style_id`) y en los diccionarios `STYLES` (`pdf/generator.py`) y `STYLES_INFO` (`contract_service.py`).
- `STYLE_NOMBRE` / `STYLE_DESCRIPCION`: **dicts** `{"es": ..., "en": ...}` con la metadata legible que se muestra en el selector de estilo del frontend, resueltos al locale pedido con `templates/i18n.pick()` en `contract_service.list_styles(locale)`.
- `apply(pdf, content) -> None`: recibe la instancia de `FPDF` (sin pagina todavia) y el `dict` de contenido, y dibuja el documento completo sobre `pdf` (agrega la pagina, fuentes, parrafos, firmas).

## Archivos

- **`style_minimal.py`**: Helvetica, margenes amplios, sin elementos decorativos.
- **`style_classic.py`**: tipografia serif (Times), titulo centrado en mayusculas con una regla fina debajo, parrafos con sangria de primera linea — convencion de documentos legales impresos.
- **`style_corporate.py`**: barra de color solida detras del titulo (`pdf.rect(..., style="F")`), estructura mas formal, firmas en negrita.
- **`style_modern.py`**: titulo grande en el color de acento con una linea corta debajo, espaciado generoso entre parrafos — jerarquia tipografica marcada en vez de color de fondo.

## Por que esta separacion

Permite que el mismo contenido (ej. el mismo NDA) se renderice con estilos distintos sin duplicar el texto, y que agregar un estilo nuevo no requiera tocar las plantillas ni el generador.
