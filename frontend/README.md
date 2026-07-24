# Frontend — Contract Generator (Vue 3 + Vite)

Wizard de 4 pasos (Tipo → Datos → Estilo → Descarga) que arma un contrato en PDF llamando al backend FastAPI. Bilingue (español/ingles) y con tema claro/oscuro, ver `src/i18n/README.md` y `src/style.css`.

## 1. Requisitos

- Node.js 20+ (`node --version` para verificar).
- El backend corriendo (ver `../backend/README.md`) — este frontend no genera nada por si solo, todo el contenido del contrato viene de la API.

## 2. Como ejecutarlo paso a paso

Todos los comandos se corren **desde la carpeta `frontend/`**.

### 2.1 Instalar las dependencias (solo la primera vez, o si `package.json` cambio)

```
npm install
```

### 2.2 Levantar el servidor de desarrollo

```
npm run dev
```

Imprime una URL, normalmente `http://localhost:5173`. Las llamadas a `/api/contracts/...` se redirigen automaticamente al backend en `http://localhost:8000` via el proxy configurado en `vite.config.ts` — no hace falta ninguna variable de entorno para desarrollo local.

Para detenerlo: `Ctrl+C` en la misma terminal.

### 2.3 Build de produccion

```
npm run build
```

Corre el chequeo de tipos (`vue-tsc -b`) y genera los archivos estaticos en `dist/`, listos para servir desde cualquier hosting estatico (Vercel, Cloudflare Pages, Netlify).

## 3. Como correr los tests

```
npm run test
```

Corre Vitest una sola vez (`vitest run`) sobre los archivos `*.spec.ts` co-ubicados junto al codigo que prueban (no en una carpeta `tests/` separada). Ver `vite.config.ts` — usa `pool: 'threads'` porque el pool por defecto (`forks`) no arranca en algunos entornos de desarrollo restringidos.

## 4. Variables de entorno

Copiar `.env.example` a `.env` solo si el backend **no** esta en `localhost:8000` (por ejemplo, para apuntar a un backend ya desplegado sin correrlo local):

- `VITE_API_BASE_URL`: URL base del backend. Sin definirla, las llamadas usan rutas relativas (`/api/contracts/...`), que funcionan en dev gracias al proxy de `vite.config.ts`. **En produccion es obligatoria** si el frontend y el backend quedan en dominios distintos (ej. frontend en Vercel, backend en Render) — sin ella, las llamadas relativas le pegarian al propio dominio del frontend, que no tiene esas rutas, y todo fallaria con 404.

Esta variable se define en el panel del hosting (ej. "Environment Variables" en Vercel), no en un `.env` commiteado.

## 5. Estructura del proyecto

```
src/
  App.vue                       # layout raiz: logo, header, toggles, wizard, footer
  main.ts                       # entrypoint, monta la app Vue
  style.css                     # variables de diseño (color, tipografia, espaciado) -> ver ../DESIGN.md
  vite-env.d.ts                 # tipado de import.meta.env (VITE_API_BASE_URL)
  components/
    contractGenerator/          # componentes del wizard -> ver README.md de la carpeta
    ui/                         # componentes genericos (botones, toggles, logo) -> ver README.md de la carpeta
  composables/contractGenerator/  # estado del wizard -> ver README.md de la carpeta
  services/contractGenerator/     # llamadas HTTP al backend -> ver README.md de la carpeta
  utils/validators/               # validacion de formularios -> ver README.md de la carpeta
  i18n/                           # idioma de la interfaz (es/en) -> ver README.md de la carpeta
```

## 6. Decisiones de arquitectura (por que esta asi)

- **`fetch` nativo, no `axios`**: pocas llamadas HTTP simples, sin interceptores ni auth compleja — una dependencia extra no se justifica.
- **Sin libreria de i18n (vue-i18n)**: un diccionario plano + un composable con estado singleton alcanza para los ~25 textos de la UI: agregar una libreria completa hubiera sido sobredimensionado para este alcance.
- **El backend traduce el contenido del contrato, el frontend traduce la UI**: son dos sistemas de i18n separados a proposito (ver `src/i18n/README.md`) — el contrato generado (legal, con vocabulario especifico) vive en el backend junto a las plantillas; los textos de botones/pasos son puramente de interfaz.
- **`VITE_API_BASE_URL` opcional (no obligatoria en dev)**: mantiene el flujo de desarrollo local en cero configuracion (`npm install && npm run dev` y ya funciona), y solo pide el dato extra cuando realmente hace falta (produccion con dominios separados).
