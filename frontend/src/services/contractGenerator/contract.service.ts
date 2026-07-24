export type Locale = 'es' | 'en'

export interface FieldSpec {
  name: string
  label: string
  placeholder: string
  type: 'text' | 'date' | 'textarea'
  max_length?: number | null
}

export interface TemplateInfo {
  id: string
  nombre: string
  descripcion: string
  icono: string
  campos: FieldSpec[]
}

export interface StyleInfo {
  id: string
  nombre: string
  descripcion: string
}

export type ContractData = Record<string, string>

export interface PreviewContent {
  titulo: string
  parrafos: string[]
  firmas: string[]
  paginas?: number
}

// Sin VITE_API_BASE_URL, queda '' y las rutas quedan relativas ('/api/...'):
// funciona en dev via el proxy de vite.config.ts. En produccion (frontend y
// backend en dominios distintos), se define esta variable con la URL real
// del backend desplegado.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

export async function fetchTemplates(locale: Locale): Promise<TemplateInfo[]> {
  const response = await fetch(`${API_BASE_URL}/api/contracts/templates?locale=${locale}`)
  if (!response.ok) throw new Error('No se pudieron cargar las plantillas')
  return response.json()
}

export async function fetchStyles(locale: Locale): Promise<StyleInfo[]> {
  const response = await fetch(`${API_BASE_URL}/api/contracts/styles?locale=${locale}`)
  if (!response.ok) throw new Error('No se pudieron cargar los estilos')
  return response.json()
}

export async function fetchPreview(
  templateId: string,
  data: ContractData,
  locale: Locale,
  styleId: string | null,
): Promise<PreviewContent> {
  const response = await fetch(`${API_BASE_URL}/api/contracts/preview`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ template_id: templateId, data, locale, style_id: styleId }),
  })
  if (!response.ok) throw new Error('No se pudo generar la vista previa')
  return response.json()
}

export async function generateContract(
  templateId: string,
  styleId: string,
  data: ContractData,
  locale: Locale,
): Promise<Blob> {
  const response = await fetch(`${API_BASE_URL}/api/contracts/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ template_id: templateId, style_id: styleId, data, locale }),
  })
  if (!response.ok) {
    // El backend manda el motivo real en el body ({"detail": "..."}, ej. un
    // campo que supera el max_length) — se muestra ese en vez de un mensaje
    // generico, si esta disponible.
    const body = await response.json().catch(() => null)
    throw new Error(body?.detail ?? 'No se pudo generar el documento')
  }
  return response.blob()
}
