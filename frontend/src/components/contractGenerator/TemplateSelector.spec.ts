import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import TemplateSelector from './TemplateSelector.vue'

const templates = [
  { id: 'nda', nombre: 'Acuerdo de Confidencialidad', descripcion: 'desc', icono: 'NDA', campos: [] },
  { id: 'contrato_laboral', nombre: 'Contrato Laboral', descripcion: 'desc', icono: 'CL', campos: [] },
]

describe('TemplateSelector', () => {
  it('marca como activa la plantilla seleccionada', () => {
    const wrapper = mount(TemplateSelector, { props: { templates, modelValue: 'nda' } })

    const opciones = wrapper.findAll('.opcion-template')
    expect(opciones[0].classes()).toContain('activo')
    expect(opciones[1].classes()).not.toContain('activo')
  })

  it('emite update:modelValue con el id de la plantilla clickeada', async () => {
    const wrapper = mount(TemplateSelector, { props: { templates, modelValue: null } })

    await wrapper.findAll('.opcion-template')[1].trigger('click')

    expect(wrapper.emitted('update:modelValue')).toEqual([['contrato_laboral']])
  })
})
