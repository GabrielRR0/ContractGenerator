# i18n

Sistema de idioma de la interfaz (español/inglés), independiente del sistema de traduccion del backend (que vive en `backend/app/services/contracts/templates/i18n.py` y traduce el *contenido del contrato*, no la UI).

## Archivos

- **`translations.ts`**: diccionario plano `{ es: {...}, en: {...} }` con todos los textos estaticos de la interfaz (titulos, botones, mensajes de error, aria-labels). Cada clave es la misma en los dos idiomas — no hay fallback automatico como en el backend, si se agrega una clave hay que traducirla en ambos bloques o TypeScript no compila.
- **`useLocale.ts`**: composable con un **singleton a nivel de modulo** (un solo `ref<Locale>` compartido por toda la app, no uno por componente). Expone:
  - `locale`: el idioma activo (`'es' | 'en'`).
  - `t`: computed con el diccionario de `translations.ts` ya resuelto al idioma activo.
  - `alternarLocale()`: cambia entre `es`/`en`.
  - Al cargar, detecta el idioma inicial: `localStorage` primero, si no hay nada guardado cae al idioma del navegador (`navigator.language`), español por defecto para cualquier idioma que no sea ingles.
  - Un `watch` persiste el cambio en `localStorage`, actualiza `document.documentElement.lang` (accesibilidad/SEO) y `document.title`.

## Por que un singleton y no Pinia/provide-inject

Es un solo valor global simple (el idioma activo) leido por casi todos los componentes — Pinia seria sobredimensionado para esto, y `provide`/`inject` obligaria a inyectarlo en cada arbol de componentes. Un modulo con estado a nivel de archivo (importado donde haga falta) alcanza y es el patron mas simple posible para este caso.

## Como interactua con el backend

El backend (plantillas, nombres, estilos) tiene su **propio** sistema de traduccion — este modulo solo le pasa el `locale` activo en cada llamada a `services/contractGenerator/contract.service.ts` (`fetchTemplates(locale)`, `fetchStyles(locale)`, etc.), pero nunca traduce contenido del contrato del lado del cliente. Ver `backend/app/services/contracts/templates/i18n.py` para el equivalente del lado del servidor.
