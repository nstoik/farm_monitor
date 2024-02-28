import { afterEach, beforeEach, describe, it, expect, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

import { APIFetch } from '@/api/fetch'
import { useGrainbinUpdateStore } from '@/stores/grainbin-update.store'

vi.mock('@/api/fetch')

describe('GraininUpdate Store', () => {
  let grainbinUpdateStore: ReturnType<typeof useGrainbinUpdateStore>
  let apiFetch: APIFetch

  beforeEach(() => {
    apiFetch = new APIFetch()
    setActivePinia(createPinia())
    grainbinUpdateStore = useGrainbinUpdateStore()
  })

  afterEach(() => {
    vi.resetAllMocks()
  })

  it('should initialize with empty grainbin updates', () => {
    expect(grainbinUpdateStore.grainbinUpdates.size).toBe(0)
  })

  it('should set grainbin updates', () => {
    const grainbinUpdate = { id: 1, grainbin: 1, temperature: 25 }
    // @ts-ignore: Ignore grainbin update type error
    grainbinUpdateStore.grainbinUpdates.set(1, grainbinUpdate)
    expect(grainbinUpdateStore.grainbinUpdates.get(1)).toEqual(grainbinUpdate)
  })

  it('should clear grainbin updates', () => {
    const grainbinUpdate = { id: 1, grainbin: 1, temperature: 25 }
    // @ts-ignore: Ignore grainbin update type error
    grainbinUpdateStore.grainbinUpdates.set(1, grainbinUpdate)
    expect(grainbinUpdateStore.grainbinUpdates.size).toBe(1)
    grainbinUpdateStore.grainbinUpdates.clear()
    expect(grainbinUpdateStore.grainbinUpdates.size).toBe(0)
  })

  describe('isLoading', () => {
    it('should set isLoading', () => {
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: [] })
      expect(grainbinUpdateStore.isLoading).toBe(false)
      grainbinUpdateStore.fetchLatestGrainbinUpdates(1)
      expect(grainbinUpdateStore.isLoading).toBe(true)
    })

    it('should clear isLoading', async () => {
      const grainbinUpdates = [{ id: 1, grainbin: 1, temperature: 25 }]
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: grainbinUpdates })
      expect(grainbinUpdateStore.isLoading).toBe(false)
      await grainbinUpdateStore.fetchLatestGrainbinUpdates(1)
      expect(grainbinUpdateStore.isLoading).toBe(false)
    })
  })

  describe('fetchLatestGrainbinUpdates', () => {
    it('should fetch grainbin updates', async () => {
      const grainbinUpdates = [
        { id: 1, grainbin: 1, temperature: 25 },
        { id: 2, grainbin: 1, temperature: 26 }
      ]
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: grainbinUpdates })
      await grainbinUpdateStore.fetchLatestGrainbinUpdates(1)
      expect(grainbinUpdateStore.grainbinUpdates.size).toBe(2)
    })

    it('should handle empty grainbin updates', async () => {
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: [] })
      await grainbinUpdateStore.fetchLatestGrainbinUpdates(1)
      expect(grainbinUpdateStore.grainbinUpdates.size).toBe(0)
    })
  })

  describe('getLatestGrainbinUpdates', () => {
    it('should get latest grainbin updates', async () => {
      const grainbinUpdates = [
        { id: 1, grainbin: 1, temperature: 25 },
        { id: 2, grainbin: 1, temperature: 26 }
      ]
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: grainbinUpdates })
      await grainbinUpdateStore.fetchLatestGrainbinUpdates(1)
      const updates = grainbinUpdateStore.getLatestGrainbinUpdates(1)
      expect(updates).toEqual(grainbinUpdates)
    })

    it('should handle empty grainbin updates', async () => {
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: [] })
      await grainbinUpdateStore.fetchLatestGrainbinUpdates(1)
      const updates = grainbinUpdateStore.getLatestGrainbinUpdates(1)
      expect(updates).toEqual([])
    })
  })
})
