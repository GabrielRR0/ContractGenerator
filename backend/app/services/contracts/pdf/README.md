# services/contracts/pdf

Toma el `dict` de contenido que arma una plantilla (`templates/*.py`) y lo renderiza como bytes de PDF, aplicando el estilo visual elegido. Es la unica parte del backend que sabe de `fpdf2`.

## Archivos

- **`generator.py`**: punto de entrada unico, `generate_pdf_bytes(style_id, content)`. Busca el modulo de estilo en el diccionario `STYLES` (por `style_id`), crea el objeto `FPDF()`, le pasa el control al estilo (`style_module.apply(pdf, content)`) y devuelve los bytes finales (`pdf.output()`). Lanza `ValueError` si el `style_id` no existe.

## Subcarpeta

- **`styles/`**: un modulo por estilo visual (tipografia, margenes, disposicion). Ver su propio README.

## Por que fpdf2 y no WeasyPrint

`fpdf2` es pure-Python: no depende de librerias nativas de sistema (Pango/Cairo/GDK-pixbuf) que WeasyPrint si necesita y que suelen fallar o inflar el cold-start en runtimes serverless (Vercel Functions / Cloudflare Workers). Esto es una restriccion explicita del proyecto (demo siempre disponible, sin cold-starts largos).
