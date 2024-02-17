<template>
  <div class="card">
    <div class="card-header text-center text-white bg-primary">
      {{ grainbin.name }}
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item">
        Average Temperature
        <div class="float-end">{{ grainbin.averageTemp }}</div>
      </li>
      <li class="list-group-item">
        Bus Number
        <div class="float-end">{{ grainbin.busNumber }}</div>
      </li>
      <li class="list-group-item">
        Sensor Type:
        <div class="float-end">{{ grainbin.sensorType }}</div>
      </li>
      <li class="list-group-item">
        Grainbin Type:
        <div class="float-end">{{ grainbin.grainbinType }}</div>
      </li>
      <li class="list-group-item">
        Updates received:
        <div class="float-end">{{ grainbin.totalUpdates }}</div>
      </li>
    </ul>
    <div class="card-footer text-center text-muted">
      Last Update:
      {{ formatDistanceToNow(grainbin.lastUpdated, { addSuffix: true }) }}
    </div>
  </div>
</template>

<script lang="ts" setup>
import { type PropType } from 'vue'
import { formatDistanceToNow } from 'date-fns/formatDistanceToNow'

import { type Grainbin } from '@/interfaces/grainbin.interface'

defineProps({
  grainbin: {
    type: Object as PropType<Grainbin>,
    required: true
  }
})
</script>
