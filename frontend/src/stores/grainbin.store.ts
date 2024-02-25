import { ref } from 'vue'
import { defineStore } from 'pinia'

import { APIFetch } from '@/api/fetch'
import { type Grainbin } from '@/interfaces/grainbin.interface'

export const useGrainbinStore = defineStore('grainbin', () => {
  const endpoint = 'grainbin/'

  const grainbins = ref<Map<Grainbin['id'], Grainbin>>(new Map())
  const isLoading = ref(false)

  /**
   * Retrieves the list of grainbins from the API.
   * @returns A promise that resolves to an array of Grainbin objects.
   */
  async function getGrainbins() {
    isLoading.value = true
    const apiFetch = new APIFetch()
    return apiFetch
      .get<Array<Grainbin>>(endpoint)
      .then((response) => {
        //convert any dates from string to Date objects
        // Add the timezone offset to the date to make it local time
        for (const key in response.data) {
          const grainbin = response.data[key]
          grainbin.lastUpdated = new Date(grainbin.lastUpdated + 'Z')
          grainbins.value.set(grainbin.id, grainbin)
        }
      })
      .finally(() => {
        isLoading.value = false
      })
  }

  /**
   * Retrieves a grainbin by its ID.
   * If the grainbin is found in the local store, it is returned.
   * Otherwise, it fetches the grainbin from the server.
   * @param id - The ID of the grainbin to retrieve.
   * @returns A Promise that resolves to the grainbin object.
   */
  async function getGrainbinByID(id: number) {
    if (grainbins.value.has(id)) {
      return grainbins.value.get(id)
    } else {
      return fetchGrainbinByID(id)
    }
  }

  async function fetchGrainbinByID(id: number) {
    // make an API request to get the grainbin by ID
    isLoading.value = true
    const apiFetch = new APIFetch()
    return apiFetch
      .get<Grainbin>(`${endpoint}${id}`)
      .then((response) => {
        // Create a grainbin object from the response data
        const grainbin = response.data
        //convert any dates from string to Date objects
        // Add the timezone offset to the date to make it local time.
        grainbin.lastUpdated = new Date(grainbin.lastUpdated + 'Z')
        // Add or update the grainbin to the grainbins array
        grainbins.value.set(grainbin.id, grainbin)
      })
      .finally(() => {
        isLoading.value = false
      })
  }

  return {
    grainbins,
    getGrainbinByID,
    getGrainbins,
    isLoading
  }
})
