/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** URL base del backend en produccion (ej. https://contract-generator-api.onrender.com).
   * Sin definir, las llamadas usan rutas relativas (funciona en dev via el
   * proxy de vite.config.ts). */
  readonly VITE_API_BASE_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
