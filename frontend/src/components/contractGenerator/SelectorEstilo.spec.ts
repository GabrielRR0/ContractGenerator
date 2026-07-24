import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import SelectorEstilo from './SelectorEstilo.vue'

const styles = [
  { id: 'minimal', nombre: 'Minimalista', descripcion: 'Sin decoracion.' },
  { id: 'corporate', nombre: 'Corporativo', descripcion: 'Mas formal.' },
]

describe('SelectorEstilo', () => {
  it('marca como activo el estilo seleccionado', () => {
    const wrapper = mount(SelectorEstilo, {
      props: { styles, modelValue: 'minimal' },
    })

    const botones = wrapper.findAll('.opcion-estilo')
    expect(botones[0].classes()).toContain('activo')
    expect(botones[1].classes()).not.toContain('activo')
  })

  it('emite update:modelValue con el id del estilo clickeado', async () => {
    const wrapper = mount(SelectorEstilo, {
      props: { styles, modelValue: 'minimal' },
    })

    await wrapper.findAll('.opcion-estilo')[1].trigger('click')

    expect(wrapper.emitted('update:modelValue')).toEqual([['corporate']])
  })
})
