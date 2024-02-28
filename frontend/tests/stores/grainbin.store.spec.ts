import { afterEach, beforeEach, describe, it, expect, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

import { APIFetch } from '@/api/fetch'
import { useGrainbinStore } from '@/stores/grainbin.store'

vi.mock('@/api/fetch')

describe('Grainbin Store', () => {
  let grainbinStore: ReturnType<typeof useGrainbinStore>
  let apiFetch: APIFetch

  beforeEach(() => {
    apiFetch = new APIFetch()
    setActivePinia(createPinia())
    grainbinStore = useGrainbinStore()
  })

  afterEach(() => {
    vi.resetAllMocks()
  })

  it('should initialize with empty grainbin', () => {
    expect(grainbinStore.grainbins.size).toBe(0)
  })

  it('should set grainbin', () => {
    const grainbin = { id: 1, name: 'Grainbin 1' }
    // @ts-ignore: Ignore grainbin type error
    grainbinStore.grainbins.set(1, grainbin)
    expect(grainbinStore.grainbins.get(1)).toEqual(grainbin)
  })

  it('should clear grainbin', () => {
    const grainbin = { id: 1, name: 'Grainbin 1' }
    // @ts-ignore: Ignore grainbin type error
    grainbinStore.grainbins.set(1, grainbin)
    expect(grainbinStore.grainbins.size).toBe(1)
    grainbinStore.grainbins.clear()
    expect(grainbinStore.grainbins.size).toBe(0)
  })

  describe('isLoading', () => {
    it('should set isLoading', () => {
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: [] })
      expect(grainbinStore.isLoading).toBe(false)
      grainbinStore.getGrainbins()
      expect(grainbinStore.isLoading).toBe(true)
    })

    it('should clear isLoading', async () => {
      const grainbins = [{ id: 1, name: 'Grainbin 1' }]
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: grainbins })
      expect(grainbinStore.isLoading).toBe(false)
      await grainbinStore.getGrainbins()
      expect(grainbinStore.isLoading).toBe(false)
    })
  })

  describe('getGrainbins', () => {
    it('should fetch grainbins', async () => {
      const grainbin = { id: 1, name: 'Grainbin 1' }
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: [grainbin] })
      await grainbinStore.getGrainbins()
      expect(grainbinStore.grainbins.size).toBe(1)
    })

    it('should fetch multiple grainbins', async () => {
      const grainbins = [
        { id: 1, name: 'Grainbin 1' },
        { id: 2, name: 'Grainbin 2' }
      ]
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: grainbins })
      await grainbinStore.getGrainbins()
      expect(grainbinStore.grainbins.size).toBe(2)
    })

    it('should handle 0 grainbins returned', async () => {
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: [] })
      await grainbinStore.getGrainbins()
      expect(grainbinStore.grainbins.size).toBe(0)
    })
  })

  describe('getGrainbinByID', () => {
    it('should fetch grainbin by ID', async () => {
      const grainbin = { id: 1, name: 'Grainbin 1' }
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      apiFetch.get.mockResolvedValueOnce({ data: grainbin })
      await grainbinStore.getGrainbinByID(1)
      expect(grainbinStore.grainbins.size).toBe(1)
      expect(grainbinStore.grainbins.get(1)).toEqual(grainbin)
    })

    it('should fetch grainbin by ID from local store', async () => {
      const grainbin = { id: 1, name: 'Grainbin 1' }
      // @ts-ignore: Ignore grainbin type error
      grainbinStore.grainbins.set(1, grainbin)
      await grainbinStore.getGrainbinByID(1)
      expect(grainbinStore.grainbins.size).toBe(1)
      expect(grainbinStore.grainbins.get(1)).toEqual(grainbin)
    })
  })
})
