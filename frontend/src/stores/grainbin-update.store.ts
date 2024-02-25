import { ref } from 'vue'
import { defineStore } from 'pinia'

import { APIFetch } from '@/api/fetch'
import { type GrainbinUpdate } from '@/interfaces/grainbin.interface'

export const useGrainbinUpdateStore = defineStore('grainbinUpdate', () => {
  const endpoint = 'grainbin/'

  const grainbinUpdates = ref<Map<GrainbinUpdate['id'], GrainbinUpdate>>(new Map())
  const isLoading = ref(false)

  async function fetchLatestGrainbinUpdates(id: number) {
    isLoading.value = true
    const apiFetch = new APIFetch()
    return apiFetch
      .get<Array<GrainbinUpdate>>(`${endpoint}${id}/updates/latest`)
      .then((response) => {
        //convert any dates from string to Date objects
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
