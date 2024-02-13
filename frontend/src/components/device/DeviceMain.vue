<template>
  <h2>Devices</h2>
  <div v-if="devices.length == 0" class="row">
    <h3>No devices found</h3>
  </div>
  <div
    v-for="device in devices"
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
import { onMounted, ref } from "vue";

import { DeviceRequest } from "@/api/device.api";
import { type Device } from "@/interfaces/device.interface";
import DeviceCard from "@/components/device/DeviceCard.vue";
import DeviceUpdate from "@/components/device/DeviceUpdate.vue";

const deviceAPI = new DeviceRequest();
const devices = ref<Array<Device>>([]);

onMounted(() => {
  deviceAPI.getDevices().then((response) => {
    devices.value = response;
  });
});
</script>
