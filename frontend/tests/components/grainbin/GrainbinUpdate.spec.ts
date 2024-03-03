import { describe, it, expect, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'

import GrainbinUpdate from '@/components/grainbin/GrainbinUpdate.vue'
import { useGrainbinUpdateStore } from '@/stores/grainbin-update.store'

/**
 * Factory function to create a wrapper for the GrainbinUpdate component.
 * @param shallow - Whether to perform a shallow mount or not. Default is false.
 * @param pinia - The Pinia instance to use for testing. Default is a new testing Pinia instance.
 * @returns A Vue wrapper for the GrainbinUpdate component.
 */
function wrapperFactory(shallow = false, pinia = createTestingPinia()) {
  return mount(GrainbinUpdate, {
    shallow: shallow,
    props: {
      grainbinID: 1
    },
    global: {
      plugins: [pinia]
    }
  })
}

describe('GrainbinUpdate', () => {
  /**
   * Initial state for the grainbinUpdateStore.
   */
  const initialState = {
    grainbinUpdate: {
      grainbinUpdates: new Map([
        [
          1,
          {
            id: 1,
            grainbin: 1,
            timestamp: new Date('2023-12-24T05:19:08.534906' + 'Z'),
            temperature: 21.875
          }
        ],
        [
          2,
          {
            id: 2,
            grainbin: 1,
            timestamp: new Date('2023-12-25T05:19:08.534906' + 'Z'),
            temperature: 22.875
          }
        ]
      ])
    }
  }

  it('renders single update properly', async () => {
    const pinia = createTestingPinia({
      createSpy: vi.fn,
      initialState: initialState
    })
    const grainbinUpdateStore = useGrainbinUpdateStore(pinia)
    // @ts-ignore: Ignore grainbin update type error
    grainbinUpdateStore.getLatestGrainbinUpdates.mockResolvedValueOnce([
      initialState.grainbinUpdate.grainbinUpdates.get(1)
    ])
    const wrapper = wrapperFactory(true, pinia)
    await flushPromises()
    expect(wrapper.text()).toContain(grainbinUpdateStore.grainbinUpdates.get(1)?.temperature)
  })

  it('renders multiple updates properly', async () => {
    const pinia = createTestingPinia({
      createSpy: vi.fn,
      initialState: initialState
    })
    const grainbinUpdateStore = useGrainbinUpdateStore(pinia)
    // @ts-ignore: Ignore grainbin update type error
    grainbinUpdateStore.getLatestGrainbinUpdates.mockResolvedValueOnce(
      Array.from(grainbinUpdateStore.grainbinUpdates.values())
    )
    const wrapper = wrapperFactory(true, pinia)
    await flushPromises()
    expect(wrapper.text()).toContain(grainbinUpdateStore.grainbinUpdates.get(1)?.temperature)
    expect(wrapper.text()).toContain(grainbinUpdateStore.grainbinUpdates.get(2)?.temperature)
    expect(grainbinUpdateStore.getLatestGrainbinUpdates).toHaveBeenCalledWith(1)
    expect(grainbinUpdateStore.grainbinUpdates.size).toBe(2)
  })

  it('renders no updates properly', async () => {
    const pinia = createTestingPinia({
      createSpy: vi.fn
    })
    const grainbinUpdateStore = useGrainbinUpdateStore(pinia)
    // @ts-ignore: Ignore grainbin update type error
    grainbinUpdateStore.getLatestGrainbinUpdates.mockResolvedValueOnce([])
    const wrapper = wrapperFactory(true, pinia)
    await flushPromises()
    expect(wrapper.text()).toContain('No updates')
  })
})
