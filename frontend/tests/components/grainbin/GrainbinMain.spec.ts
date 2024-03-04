import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'

import GrainbinMain from '@/components/grainbin/GrainbinMain.vue'

/**
 * Factory function to create a wrapper for the GrainbinMain component.
 * @param shallow - Flag indicating whether to perform a shallow mount.
 * @param initialState - Initial state for the testing Pinia store.
 * @returns A mounted wrapper for the GrainbinMain component.
 */
function wrapperFactory(shallow = false, initialState = {}) {
  return mount(GrainbinMain, {
    shallow: shallow,
    global: {
      plugins: [
        createTestingPinia({
          createSpy: vi.fn,
          initialState: initialState
        })
      ]
    }
  })
}

describe('GrainbinMain', () => {
  it('renders properly', () => {
    const wrapper = wrapperFactory()
    expect(wrapper.text()).toContain('No grainbins found')
  })

  it('renders grainbins', () => {
    const initialState = {
      grainbin: {
        grainbins: new Map([[1, { id: 1, name: 'Grainbin 1', lastUpdated: new Date() }]])
      }
    }
    const wrapper = wrapperFactory(true, initialState)
    expect(wrapper.html()).toContain('grainbinid="1"')
  })
})
