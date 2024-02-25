import { ref } from 'vue'
import { defineStore } from 'pinia'

import { APIFetch } from '@/api/fetch'
import { type DeviceUpdate } from '@/interfaces/device.interface'

export const useDeviceUpdateStore = defineStore('deviceUpdate', () => {
  const endpoint = 'device/'

  const deviceUpdates = ref<Map<DeviceUpdate['id'], DeviceUpdate>>(new Map())
  const isLoading = ref(false)

  async function fetchLatestDeviceUpdate(id: number) {
    isLoading.value = true
    const apiFetch = new APIFetch()
    return apiFetch
      .get<DeviceUpdate>(`${endpoint}${id}/updates/latest`)
      .then((response) => {
        //convert any dates from string to Date objects
        const deviceUpdate = response.data
        deviceUpdate.timestamp = new Date(deviceUpdate.timestamp + 'Z')
        deviceUpdates.value.set(deviceUpdate.id, deviceUpdate)
      })
      .finally(() => {
        isLoading.value = false
      })
  }

  async function fetchDeviceUpdatePagination(id: number, page = 1, pageSize = 10) {
    isLoading.value = true
    const apiFetch = new APIFetch()

    return apiFetch
      .getPaginate<DeviceUpdate>(`${endpoint}${id}/updates`, page, pageSize)
      .then(([response, paginationHeaderResponse]) => {
        //convert any dates from string to Date objects
        for (const key in response.data) {
          const deviceUpdate = response.data[key]
          deviceUpdate.timestamp = new Date(deviceUpdate.timestamp + 'Z')
          deviceUpdates.value.set(deviceUpdate.id, deviceUpdate)
        }
        return paginationHeaderResponse
      })
      .finally(() => {
        isLoading.value = false
      })
  }

  function getLatestDeviceUpdates(device: number) {
    const updates = Array.from(deviceUpdates.value.values()).filter(
      (update) => update.device === device
    )
    return updates
  }

  return {
    deviceUpdates,
    getLatestDeviceUpdates,
    fetchDeviceUpdatePagination,
    fetchLatestDeviceUpdate,
    isLoading
  }
})
