<template>
  <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <th>Measurement Taken</th>
        <th>Interior Temp</th>
        <th>Exterior Temp</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="update in deviceUpdates" :key="update.updateIndex">
        <td>
          {{ formatDistanceToNow(update.timestamp, { addSuffix: true }) }}
        </td>
        <td>{{ update.interiorTemp }}</td>
        <td>{{ update.exteriorTemp }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { formatDistanceToNow } from 'date-fns/formatDistanceToNow'

import { useDeviceUpdateStore } from '@/stores/device-update.store'
import { type DeviceUpdate } from '@/interfaces/device.interface'

const props = defineProps({
  deviceID: {
    type: Number,
    required: true
  }
})

const startingPage = 1
const pageSize = 10

const deviceUpdateStore = useDeviceUpdateStore()
const deviceUpdates = ref<Array<DeviceUpdate>>([])

onMounted(() => {
  deviceUpdateStore.fetchDeviceUpdatePagination(props.deviceID, startingPage, pageSize).then(() => {
    deviceUpdates.value = deviceUpdateStore.getLatestDeviceUpdates(props.deviceID)
  })
})
</script>
