import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'

import GrainbinMain from '@/components/grainbin/GrainbinMain.vue'

describe('GrainbinMain', () => {
  it('renders properly', () => {
    const wrapper = mount(GrainbinMain, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn
          })
        ]
      }
    })
    expect(wrapper.text()).toContain('No grainbins found')
  })
})
