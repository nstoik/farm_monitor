<template>
  <h2>Grainbins</h2>
  <div v-if="grainbinStore.grainbins.size == 0" class="row">
    <h3>No grainbins found</h3>
  </div>
  <div
    v-for="grainbin in grainbinStore.grainbins.values()"
    :key="grainbin.id"
    class="row align-items-start g-3 mb-3"
  >
    <div class="col-md-12 col-lg-4">
      <grainbin-card :grainbin="grainbin" />
    </div>
    <div class="col-md-12 col-lg-8">
      <grainbin-update :grainbinID="grainbin.id" />
    </div>
    <hr class="border border-primary border-4 border-top" />
  </div>
</template>

<script lang="ts" , setup>
import { onMounted } from 'vue'

import GrainbinCard from '@/components/grainbin/GrainbinCard.vue'
import GrainbinUpdate from '@/components/grainbin/GrainbinUpdate.vue'
import { useGrainbinStore } from '@/stores/grainbin.store'

const grainbinStore = useGrainbinStore()

onMounted(() => {
  grainbinStore.getGrainbins()
})
</script>
