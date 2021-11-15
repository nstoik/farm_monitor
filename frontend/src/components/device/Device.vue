<template>
  <h2>Devices</h2>
  <div class="row">
    <div v-if="devices.length == 0">No devices found.</div>
    <div v-else>
      <div class="col-md-12 col-lg-6 col-xl-4" v-for="device in devices" :key="device.id">
        <device-card :device="device" />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { DeviceRequest } from "@/api/device.api";
import { Device } from "@/interfaces/device.interface";
import DeviceCard from "@/components/device/DeviceCard.vue";

const deviceAPI = new DeviceRequest();
const devices = ref<Array<Device>>([]);

onMounted(() => {
  deviceAPI.getDevices().then((response) => {
    devices.value = response;
  });
});
</script>
