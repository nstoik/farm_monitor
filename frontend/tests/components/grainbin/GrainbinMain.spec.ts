import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import GrainbinMain from '../../../src/components/grainbin/GrainbinMain.vue'

describe('GrainbinMain', () => {
  it('renders properly', () => {
    const wrapper = mount(GrainbinMain)
    expect(wrapper.text()).toContain('No grainbins found')
  })
})
