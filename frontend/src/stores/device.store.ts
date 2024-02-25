import { ref } from 'vue'
import { defineStore } from 'pinia'

import { APIFetch } from '@/api/fetch'
import { type Device } from '@/interfaces/device.interface'

export const useDeviceStore = defineStore('device', () => {
  const endpoint = 'device/'

  const devices = ref<Map<Device['id'], Device>>(new Map())
  const isLoading = ref(false)

  async function getDevices() {
    isLoading.value = true
    const apiFetch = new APIFetch()
    return apiFetch
      .get<Array<Device>>(endpoint)
      .then((response) => {
        for (const key in response.data) {
          const device = response.data[key]
          device.lastUpdateReceived = new Date(device.lastUpdateReceived + 'Z')
          device.lastUpdated = new Date(device.lastUpdated + 'Z')
          devices.value.set(device.id, device)
        }
      })
      .finally(() => {
        isLoading.value = false
      })
  }
  return {
    devices,
    getDevices,
    isLoading
  }
})
