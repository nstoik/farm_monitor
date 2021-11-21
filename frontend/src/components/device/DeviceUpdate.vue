<template>
  <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <th>Timestamp</th>
        <th>Interior Temp</th>
        <th>Exterior Temp</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="update in deviceUpdates" :key="update.updateIndex">
        <td>{{ update.timestamp }}</td>
        <td>{{ update.interiorTemp }}</td>
        <td>{{ update.exteriorTemp }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script lang="ts" setup>
import { defineProps, onMounted, ref } from "vue";
import { DeviceRequest } from "@/api/device.api";
import { DeviceUpdate } from "@/interfaces/device.interface";

const props = defineProps({
  deviceID: {
    type: Number,
    required: true,
  },
});

const startingPage = 1;
const pageSize = 3;

const deviceAPI = new DeviceRequest();
const deviceUpdates = ref<Array<DeviceUpdate>>([]);

onMounted(() => {
  deviceAPI
    .getDeviceUpdates(props.deviceID, startingPage, pageSize)
    .then((response) => {
      deviceUpdates.value = response[0];
    });
});
</script>
