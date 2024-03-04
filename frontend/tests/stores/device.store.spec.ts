import { afterEach, beforeEach, describe, it, expect, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

import { APIFetch } from '@/api/fetch'
import { useDeviceStore } from '@/stores/device.store'

vi.mock('@/api/fetch')

describe('Device Store', () => {
  let deviceStore: ReturnType<typeof useDeviceStore>
  let apiFetch: APIFetch

  beforeEach(() => {
    apiFetch = new APIFetch()
    setActivePinia(createPinia())
    deviceStore = useDeviceStore()
  })

  afterEach(() => {
    vi.resetAllMocks()
  })

  it('should initialize with empty devices', () => {
    expect(deviceStore.devices.size).toBe(0)
  })

  it('should set devices', () => {
    const device = { id: 1, name: 'Device 1' }
    // @ts-ignore: Ignore device type error
    deviceStore.devices.set(1, device)
    expect(deviceStore.devices.get(1)).toEqual(device)
  })

  it('should clear devices', () => {
    const device = { id: 1, name: 'Device 1' }
    // @ts-ignore: Ignore device type error
    deviceStore.devices.set(1, device)
    expect(deviceStore.devices.size).toBe(1)
    deviceStore.devices.clear()
    expect(deviceStore.devices.size).toBe(0)
  })

  describe('isLoading', () => {
    it('should set isLoading', () => {
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: [] })
      expect(deviceStore.isLoading).toBe(false)
      deviceStore.getDevices()
      expect(deviceStore.isLoading).toBe(true)
    })

    it('should clear isLoading', async () => {
      const devices = [{ id: 1, name: 'Device 1' }]
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: devices })
      expect(deviceStore.isLoading).toBe(false)
      await deviceStore.getDevices()
      expect(deviceStore.isLoading).toBe(false)
    })
  })

  describe('getDevices', () => {
    it('should fetch devices', async () => {
      const devices = [{ id: 1, name: 'Device 1' }]
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: devices })
      await deviceStore.getDevices()
      expect(deviceStore.devices.size).toBe(1)
      expect(deviceStore.devices.get(1)).toEqual(devices[0])
    })

    it('should fetch multiple devices', async () => {
      const devices = [
        { id: 1, name: 'Device 1' },
        { id: 2, name: 'Device 2' }
      ]
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: devices })
      await deviceStore.getDevices()
      expect(deviceStore.devices.size).toBe(2)
      expect(deviceStore.devices.get(1)).toEqual(devices[0])
      expect(deviceStore.devices.get(2)).toEqual(devices[1])
    })
  })
})
