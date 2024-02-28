import { ref } from 'vue'
import { defineStore } from 'pinia'

import { APIFetch } from '@/api/fetch'
import { type DeviceUpdate } from '@/interfaces/device.interface'

export const useDeviceUpdateStore = defineStore('deviceUpdate', () => {
  const endpoint = 'device/'

  const deviceUpdates = ref<Map<DeviceUpdate['id'], DeviceUpdate>>(new Map())
  const isLoading = ref(false)

  /**
   * Fetches the latest device update for a given ID.
   * @param id - The ID of the device.
   * @returns A Promise that resolves to the fetched device update being stored.
   */
  async function fetchLatestDeviceUpdate(id: number) {
    isLoading.value = true
    const apiFetch = new APIFetch()
    return apiFetch
      .get<DeviceUpdate>(`${endpoint}${id}/updates/latest`)
      .then((response) => {
        const deviceUpdate = response.data
        deviceUpdate.timestamp = new Date(deviceUpdate.timestamp + 'Z')
        deviceUpdates.value.set(deviceUpdate.id, deviceUpdate)
      })
      .finally(() => {
        isLoading.value = false
      })
  }

  /**
   * Fetches device updates with pagination.
   *
   * @param id - The ID of the device.
   * @param page - The page number to fetch (default: 1).
   * @param pageSize - The number of items per page (default: 10).
   * @returns A Promise that resolves to the pagination header response.
   */
  async function fetchDeviceUpdatePagination(id: number, page = 1, pageSize = 10) {
    isLoading.value = true
    const apiFetch = new APIFetch()

    return apiFetch
      .getPaginate<DeviceUpdate>(`${endpoint}${id}/updates`, page, pageSize)
      .then(([response, paginationHeaderResponse]) => {
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

  /**
   * Retrieves the latest device updates for a given device.
   * @param device - The device number.
   * @returns An array of device updates.
   */
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
