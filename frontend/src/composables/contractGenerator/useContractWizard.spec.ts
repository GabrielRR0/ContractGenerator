import { flushPromises } from '@vue/test-utils'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { createApp } from 'vue'
import { useLocale } from '../../i18n/useLocale'
import { useContractWizard } from './useContractWizard'

const TEMPLATES = [
  {
    id: 'nda',
    nombre: 'Acuerdo de Confidencialidad',
    descripcion: 'desc',
    icono: 'NDA',
    campos: [
      { name: 'parte_reveladora', label: 'Parte reveladora', placeholder: '', type: 'text' },
      { name: 'parte_receptora', label: 'Parte receptora', placeholder: '', type: 'text' },
    ],
  },
]

const STYLES = [{ id: 'minimal', nombre: 'Minimalista', descripcion: 'desc' }]

function mockFetch() {
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string) => {
      if (url.includes('/templates')) return { ok: true, json: async () => TEMPLATES }
      if (url.includes('/styles')) return { ok: true, json: async () => STYLES }
      if (url.includes('/preview')) {
        return { ok: true, json: async () => ({ titulo: 'x', parrafos: ['p'], firmas: [] }) }
      }
      return { ok: true, json: async () => ({}) }
    }),
  )
}

// onMounted solo se registra dentro de un componente activo: se monta el
// composable en un componente vacio para que su ciclo de vida corra de verdad.
function montarWizard() {
  let resultado!: ReturnType<typeof useContractWizard>
  const app = createApp({
    setup() {
      resultado = useContractWizard()
      return () => null
    },
  })
  app.mount(document.createElement('div'))
  return resultado
}

describe('useContractWizard', () => {
  beforeEach(() => {
    mockFetch()
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('no avanza del paso 1 si no se eligio un tipo de contrato', async () => {
    const wizard = montarWizard()
    await flushPromises()

    wizard.siguiente()

    expect(wizard.paso.value).toBe(1)
    expect(wizard.errores.value.length).toBeGreaterThan(0)
  })

  it('avanza al paso 2 al elegir un tipo, y no avanza al 3 si faltan campos', async () => {
    const wizard = montarWizard()
    await flushPromises()

    wizard.templateId.value = 'nda'
    wizard.siguiente()
    expect(wizard.paso.value).toBe(2)

    wizard.siguiente()
    expect(wizard.paso.value).toBe(2)
    expect(wizard.errores.value.length).toBeGreaterThan(0)
  })

  it('avanza hasta el paso 3 con los datos completos', async () => {
    const wizard = montarWizard()
    await flushPromises()

    wizard.templateId.value = 'nda'
    wizard.siguiente()
    wizard.data.parte_reveladora = 'Acme S.A.'
    wizard.data.parte_receptora = 'Juan Perez'
    wizard.siguiente()

    expect(wizard.paso.value).toBe(3)
  })

  it('anterior() retrocede un paso', async () => {
    const wizard = montarWizard()
    await flushPromises()

    wizard.templateId.value = 'nda'
    wizard.siguiente()
    expect(wizard.paso.value).toBe(2)

    wizard.anterior()
    expect(wizard.paso.value).toBe(1)
  })

  it('vuelve a pedir templates/styles al cambiar de idioma', async () => {
    const { locale } = useLocale()
    locale.value = 'es'
    const fetchMock = vi.fn(async (url: string) => {
      if (url.includes('/templates')) return { ok: true, json: async () => TEMPLATES }
      if (url.includes('/styles')) return { ok: true, json: async () => STYLES }
      return { ok: true, json: async () => ({}) }
    })
    vi.stubGlobal('fetch', fetchMock)

    montarWizard()
    await flushPromises()
    const llamadasIniciales = fetchMock.mock.calls.length

    locale.value = 'en'
    await flushPromises()

    const urlsLlamadas = fetchMock.mock.calls.slice(llamadasIniciales).map((llamada) => llamada[0] as string)
    expect(urlsLlamadas.some((url) => url.includes('/templates?locale=en'))).toBe(true)
    expect(urlsLlamadas.some((url) => url.includes('/styles?locale=en'))).toBe(true)
  })
})
