import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'

function setNavigatorLanguage(idioma: string) {
  Object.defineProperty(navigator, 'language', { value: idioma, configurable: true })
}

describe('useLocale', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.resetModules()
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('detecta espanol por defecto si el navegador no esta en ingles', async () => {
    setNavigatorLanguage('es-AR')
    const { useLocale } = await import('./useLocale')
    const { locale } = useLocale()
    expect(locale.value).toBe('es')
  })

  it('detecta ingles si el navegador esta en ingles', async () => {
    setNavigatorLanguage('en-US')
    const { useLocale } = await import('./useLocale')
    const { locale } = useLocale()
    expect(locale.value).toBe('en')
  })

  it('respeta el idioma guardado en localStorage por sobre el navegador', async () => {
    localStorage.setItem('locale', 'en')
    setNavigatorLanguage('es-AR')
    const { useLocale } = await import('./useLocale')
    const { locale } = useLocale()
    expect(locale.value).toBe('en')
  })

  it('alternarLocale cambia entre es y en, y persiste en localStorage', async () => {
    setNavigatorLanguage('es-AR')
    const { useLocale } = await import('./useLocale')
    const { locale, alternarLocale } = useLocale()

    expect(locale.value).toBe('es')
    alternarLocale()
    await nextTick() // el watcher que persiste a localStorage corre en el siguiente tick
    expect(locale.value).toBe('en')
    expect(localStorage.getItem('locale')).toBe('en')
  })

  it('t expone los textos traducidos del locale activo', async () => {
    setNavigatorLanguage('en-US')
    const { useLocale } = await import('./useLocale')
    const { t } = useLocale()

    expect(t.value.continueButton).toBe('Continue')
  })
})
