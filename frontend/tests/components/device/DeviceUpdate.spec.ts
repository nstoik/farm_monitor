import { describe, it, expect, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'

import DeviceUpdate from '@/components/device/DeviceUpdate.vue'
import { useDeviceUpdateStore } from '@/stores/device-update.store'

/**
 * Factory function to create a wrapper for the GrainbinUpdate component.
 * @param shallow - Whether to perform a shallow mount or not. Default is false.
 * @param pinia - The Pinia instance to use for testing. Default is a new testing Pinia instance.
 * @returns A Vue wrapper for the GrainbinUpdate component.
 */
function wrapperFactory(shallow = false, pinia = createTestingPinia()) {
  return mount(DeviceUpdate, {
    shallow: shallow,
    props: {
      deviceID: 1
    },
    global: {
      plugins: [pinia]
    }
  })
}

describe('DeviceUpdate', () => {
  /**
   * Initial state for the deviceUpdateStore.
   */
  const initialState = {
    deviceUpdate: {
      deviceUpdates: new Map([
        [
          1,
          {
            id: 1,
            device: 1,
            timestamp: new Date('2023-12-24T05:19:08.534906' + 'Z'),
            interiorTemp: 21.875
          }
        ],
        [
          2,
          {
            id: 2,
            device: 1,
            timestamp: new Date('2023-12-25T05:19:08.534906' + 'Z'),
            interiorTemp: 22.875
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
    const deviceUpdateStore = useDeviceUpdateStore(pinia)
    // @ts-ignore: Ignore grainbin update type error
    deviceUpdateStore.getLatestDeviceUpdates.mockResolvedValueOnce([
      initialState.deviceUpdate.deviceUpdates.get(1)
    ])
    const wrapper = wrapperFactory(true, pinia)
    await flushPromises()
    expect(wrapper.text()).toContain(deviceUpdateStore.deviceUpdates.get(1)?.interiorTemp)
  })

  it('renders multiple updates properly', async () => {
    const pinia = createTestingPinia({
      createSpy: vi.fn,
      initialState: initialState
    })
    const deviceUpdateStore = useDeviceUpdateStore(pinia)
    // @ts-ignore: Ignore grainbin update type error
    deviceUpdateStore.getLatestDeviceUpdates.mockResolvedValueOnce(
      Array.from(deviceUpdateStore.deviceUpdates.values())
    )
    const wrapper = wrapperFactory(true, pinia)
    await flushPromises()
    expect(wrapper.text()).toContain(deviceUpdateStore.deviceUpdates.get(1)?.interiorTemp)
    expect(wrapper.text()).toContain(deviceUpdateStore.deviceUpdates.get(2)?.interiorTemp)
    expect(deviceUpdateStore.getLatestDeviceUpdates).toHaveBeenCalledWith(1)
    expect(deviceUpdateStore.deviceUpdates.size).toBe(2)
  })

  it('renders no updates properly', async () => {
    const pinia = createTestingPinia({
      createSpy: vi.fn
    })
    const deviceUpdateStore = useDeviceUpdateStore(pinia)
    // @ts-ignore: Ignore grainbin update type error
    deviceUpdateStore.getLatestDeviceUpdates.mockResolvedValueOnce([])
    const wrapper = wrapperFactory(true, pinia)
    await flushPromises()
    expect(wrapper.text()).toContain('No updates')
  })
})
