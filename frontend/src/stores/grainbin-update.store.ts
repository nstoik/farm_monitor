import { ref } from 'vue'
import { defineStore } from 'pinia'

import { APIFetch } from '@/api/fetch'
import { type GrainbinUpdate } from '@/interfaces/grainbin.interface'

export const useGrainbinUpdateStore = defineStore('grainbinUpdate', () => {
  const endpoint = 'grainbin/'

  const grainbinUpdates = ref<Map<GrainbinUpdate['id'], GrainbinUpdate>>(new Map())
  const isLoading = ref(false)

  /**
   * Fetches the latest grainbin updates for a given ID.
   * @param id - The ID of the grain bin.
   * @returns A Promise that resolves to the fetched grainbin update being stored.
   */
  async function fetchLatestGrainbinUpdates(id: number) {
    isLoading.value = true
    const apiFetch = new APIFetch()
    return apiFetch
      .get<Array<GrainbinUpdate>>(`${endpoint}${id}/updates/latest`)
      .then((response) => {
        for (const key in response.data) {
          const grainbinUpdate = response.data[key]
          grainbinUpdate.timestamp = new Date(grainbinUpdate.timestamp + 'Z')
          grainbinUpdates.value.set(grainbinUpdate.id, grainbinUpdate)
        }
      })
      .finally(() => {
        isLoading.value = false
      })
  }

  /**
   * Retrieves the latest grain bin updates for a specific grain bin.
   * @param grainbin The ID of the grain bin.
   * @returns An array of the latest grain bin updates.
   */
  function getLatestGrainbinUpdates(grainbin: number) {
    const updates = Array.from(grainbinUpdates.value.values()).filter(
      (update) => update.grainbin === grainbin
    )
    return updates
  }

  return {
    grainbinUpdates,
    getLatestGrainbinUpdates,
    fetchLatestGrainbinUpdates,
    isLoading
  }
})
