<template>
  <div class="card">
    <div class="card-header text-center text-white bg-primary">
      {{ device.name }}
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item">
        Number of grainbins:
        <div class="float-end">{{ device.grainbinCount }}</div>
      </li>
      <li class="list-group-item">
        Location:
        <div class="float-end">{{ device.location }}</div>
      </li>
      <li class="list-group-item">
        Updates received:
        <div class="float-end">{{ device.totalUpdates }}</div>
      </li>
    </ul>
    <div class="card-footer text-center text-muted">
      Last Update: {{ device.lastUpdateReceived }}
    </div>
  </div>
</template>

<script lang="ts" setup>
import { defineProps, PropType } from "vue";

import { Device } from "@/interfaces/device.interface";

defineProps({
  device: {
    type: Object as PropType<Device>,
    required: true,
  },
});
</script>
