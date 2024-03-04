<template>
  <h2>Devices</h2>
  <div v-if="deviceStore.devices.size == 0" class="row">
    <h3>No devices found</h3>
  </div>
  <div
    v-for="device in deviceStore.devices.values()"
    :key="device.id"
    class="row align-items-start g-3"
  >
    <div class="col-md-12 col-lg-6 col-xl-3">
      <device-card :device="device" />
    </div>
    <div class="col-md-12 col-lg-6 col-xl-3">
      <device-update :deviceID="device.id" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue'

import DeviceCard from '@/components/device/DeviceCard.vue'
import DeviceUpdate from '@/components/device/DeviceUpdate.vue'
import { useDeviceStore } from '@/stores/device.store'

const deviceStore = useDeviceStore()

onMounted(() => {
  deviceStore.getDevices()
})
</script>
