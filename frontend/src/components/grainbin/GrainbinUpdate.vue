<template>
  <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <th>Measurement Taken</th>
        <th>Cable Number</th>
        <th>Sensor Number</th>
        <th>Temperature</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="update in grainbinUpdates" :key="update.id">
        <td>
          {{ formatDistanceToNow(update.timestamp, { addSuffix: true }) }}
        </td>
        <td>{{ update.temphigh }}</td>
        <td>{{ update.templow }}</td>
        <td>{{ update.temperature }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { formatDistanceToNow } from 'date-fns/formatDistanceToNow'

import { useGrainbinUpdateStore } from '@/stores/grainbin-update.store'
import { type GrainbinUpdate } from '@/interfaces/grainbin.interface'

const props = defineProps({
  grainbinID: {
    type: Number,
    required: true
  }
})

const grainbinUpdateStore = useGrainbinUpdateStore()

let grainbinUpdates = ref(Array<GrainbinUpdate>())

onMounted(() => {
  grainbinUpdateStore.fetchLatestGrainbinUpdates(props.grainbinID).then(() => {
    grainbinUpdates.value = grainbinUpdateStore.getLatestGrainbinUpdates(props.grainbinID)
  })
})
</script>
