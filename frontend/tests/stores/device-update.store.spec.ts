import { afterEach, beforeEach, describe, it, expect, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

import { APIFetch, type PaginationHeader } from '@/api/fetch'
import { useDeviceUpdateStore } from '@/stores/device-update.store'

vi.mock('@/api/fetch')

describe('DeviceUpdate Store', () => {
  let deviceUpdateStore: ReturnType<typeof useDeviceUpdateStore>
  let apiFetch: APIFetch

  beforeEach(() => {
    apiFetch = new APIFetch()
    setActivePinia(createPinia())
    deviceUpdateStore = useDeviceUpdateStore()
  })

  afterEach(() => {
    vi.resetAllMocks()
  })

  it('should initialize with empty device updates', () => {
    expect(deviceUpdateStore.deviceUpdates.size).toBe(0)
  })

  it('should set device updates', () => {
    const deviceUpdate = { id: 1, device: 1, temperature: 25 }
    // @ts-ignore: Ignore device update type error
    deviceUpdateStore.deviceUpdates.set(1, deviceUpdate)
    expect(deviceUpdateStore.deviceUpdates.get(1)).toEqual(deviceUpdate)
  })

  it('should clear device updates', () => {
    const deviceUpdate = { id: 1, device: 1, temperature: 25 }
    // @ts-ignore: Ignore device update type error
    deviceUpdateStore.deviceUpdates.set(1, deviceUpdate)
    expect(deviceUpdateStore.deviceUpdates.size).toBe(1)
    deviceUpdateStore.deviceUpdates.clear()
    expect(deviceUpdateStore.deviceUpdates.size).toBe(0)
  })

  describe('isLoading', () => {
    it('should set isLoading', () => {
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: [] })
      expect(deviceUpdateStore.isLoading).toBe(false)
      deviceUpdateStore.fetchLatestDeviceUpdate(1)
      expect(deviceUpdateStore.isLoading).toBe(true)
    })

    it('should clear isLoading', async () => {
      const deviceUpdates = [{ id: 1, device: 1, temperature: 25 }]
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: deviceUpdates })
      expect(deviceUpdateStore.isLoading).toBe(false)
      await deviceUpdateStore.fetchLatestDeviceUpdate(1)
      expect(deviceUpdateStore.isLoading).toBe(false)
    })
  })

  describe('fetchLatestDeviceUpdate', () => {
    afterEach(() => {
      deviceUpdateStore.deviceUpdates.clear()
    })

    it('should fetch the latest device update', async () => {
      const deviceUpdate = { id: 1, device: 1, temperature: 25 }
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: deviceUpdate })
      await deviceUpdateStore.fetchLatestDeviceUpdate(1)
      expect(deviceUpdateStore.deviceUpdates.get(1)).toEqual(deviceUpdate)
    })

    it('should handle empty device updates', async () => {
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: null })
      await deviceUpdateStore.fetchLatestDeviceUpdate(1)
      expect(deviceUpdateStore.deviceUpdates.size).toBe(0)
    })
  })

  describe('getLatestDeviceUpdates', () => {
    it('should get latest device updates', async () => {
      const deviceUpdate = { id: 1, device: 1, temperature: 25 }
      // @ts-ignore: Ignore device update type error
      deviceUpdateStore.deviceUpdates.set(1, deviceUpdate)
      const updates = deviceUpdateStore.getLatestDeviceUpdates(1)
      expect(updates).toEqual([deviceUpdate])
    })

    it('should handle empty device updates', async () => {
      const updates = deviceUpdateStore.getLatestDeviceUpdates(1)
      expect(updates).toEqual([])
    })
  })

  describe('fetchDeviceUpdatePagination', () => {
    const paginationHeaderResponse: PaginationHeader = {
      total: 100,
      totalPages: 5,
      firstPage: 1,
      lastPage: 5,
      page: 2
    }
    it('should fetch device updates with pagination', async () => {
      const deviceUpdates = [
        { id: 1, device: 1, temperature: 25 },
        { id: 2, device: 1, temperature: 26 }
      ]
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.getPaginate.mockResolvedValueOnce([{ data: deviceUpdates }])
      await deviceUpdateStore.fetchDeviceUpdatePagination(1)
      expect(deviceUpdateStore.deviceUpdates.size).toBe(2)
    })

    it('should handle empty device updates', async () => {
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.getPaginate.mockResolvedValueOnce([{ data: [] }, { link: 'link' }])
      await deviceUpdateStore.fetchDeviceUpdatePagination(1)
      expect(deviceUpdateStore.deviceUpdates.size).toBe(0)
    })

    it('should return pagination header response', async () => {
      const deviceUpdates = [
        { id: 1, device: 1, temperature: 25 },
        { id: 2, device: 1, temperature: 26 }
      ]
      const response = { data: deviceUpdates }
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.getPaginate.mockResolvedValueOnce([response, paginationHeaderResponse])
      const pagination = await deviceUpdateStore.fetchDeviceUpdatePagination(1)
      expect(pagination).toEqual(paginationHeaderResponse)
      expect(deviceUpdateStore.deviceUpdates.size).toBe(2)
    })
  })
})
