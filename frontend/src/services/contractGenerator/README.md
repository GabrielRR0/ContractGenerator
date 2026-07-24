# services/contractGenerator

Capa de acceso HTTP al backend. Es el unico lugar del frontend que sabe la forma de las rutas de la API (`/api/contracts/...`) — los componentes y composables nunca llaman `fetch` directamente.

## Archivos

- **`contract.service.ts`**: define los tipos que espejan los schemas de Pydantic del backend (`FieldSpec`, `TemplateInfo`, `StyleInfo`, `ContractData`, `PreviewContent`, `Locale`) y 4 funciones, todas reciben el `locale` activo (`'es' | 'en'`, ver `i18n/useLocale.ts`) para que el backend responda ya traducido:
  - `fetchTemplates(locale)` / `fetchStyles(locale)`: `GET` a los catalogos (`locale` como query param), usados por `useContractWizard` para poblar el selector de tipo y de estilo.
  - `fetchPreview(templateId, data, locale)`: `POST /api/contracts/preview`, devuelve el contenido textual (`titulo`/`parrafos`/`firmas`) ya en el idioma pedido, tolerante a datos incompletos, para el preview en vivo.
  - `generateContract(templateId, styleId, data, locale)`: `POST /api/contracts/generate`, devuelve un `Blob` (el PDF binario, en el idioma pedido) listo para descargar con `URL.createObjectURL`.

  Este archivo no traduce nada por su cuenta — solo reenvia el `locale` que le pasa quien lo llama. Toda la logica de idioma del contenido vive en el backend (`templates/i18n.py`).

## Por que `fetch` nativo y no `axios`

Con solo 4 llamadas HTTP simples (sin interceptores ni auth compleja) no se justifica una dependencia extra — `fetch` alcanza y mantiene el bundle liviano.

## Por que en dev funciona sin configurar la URL del backend

`vite.config.ts` define un proxy de `/api` hacia `http://localhost:8000`, asi que estas funciones usan rutas relativas (`/api/contracts/...`) tanto en dev como en produccion (donde el proxy se reemplaza por la configuracion de rewrite del hosting, ej. Vercel).
