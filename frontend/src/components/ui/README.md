# components/ui

Componentes visuales reutilizables sin dominio propio (no saben nada de "contratos" ni de ningun otro feature). Se comparten entre features via slots/props genericos.

## Archivos

- **`BaseButton.vue`**: boton estilizado con estado `disabled`, evento `click` y `variant` (`primary` por defecto, `secondary` para el boton "Atrás" del wizard — borde sin relleno en vez del acento solido).
- **`BaseCard.vue`**: contenedor visual (borde redondeado, padding) usado para agrupar cada paso del wizard en `ContractGeneratorMain.vue`.
- **`ThemeToggle.vue`**: switch manual de tema claro/oscuro (sol/luna). Al montar, lee `localStorage` o `prefers-color-scheme` como fallback; al hacer click, escribe `data-theme="light"/"dark"` en `<html>` (lo consume `style.css` con selectores `:root[data-theme=...]`, que tienen prioridad sobre la media query del sistema) y persiste la eleccion en `localStorage`.
- **`AppLogo.vue`**: badge cuadrado con el icono de documento del proyecto (mismo SVG que `public/favicon.svg`, reescalado). Usa `currentColor` para el trazo, asi hereda el color de texto que le da el contenedor — no hace falta una version por tema.
- **`AppFooter.vue`**: pie de pagina minimo con el link a LinkedIn del autor. Intencionalmente discreto (icono chico, opacidad reducida hasta hover) — no es un footer de marketing con links de navegacion, solo una firma.
- **`LanguageToggle.vue`**: switch manual de idioma (ES/EN), hermano visual de `ThemeToggle.vue`. Usa el composable `useLocale` (`i18n/useLocale.ts`) — no tiene estado propio, solo llama a `alternarLocale()`.

## Por que estan separados de `contractGenerator/`

Si se agrega un segundo feature en este proyecto (o en otro sub-proyecto del portafolio que comparta este mismo frontend), estos componentes no deberian duplicarse — viven en `ui/` justamente porque no dependen del dominio de contratos.
