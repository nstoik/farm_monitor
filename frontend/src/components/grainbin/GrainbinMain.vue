<template>
  <h2>Grainbins</h2>
  <div v-if="grainbins.length == 0" class="row">
    <h3>No grainbins found</h3>
  </div>
  <div
    v-for="grainbin in grainbins"
    :key="grainbin.id"
    class="row align-items-start g-3 mb-3"
  >
    <div class="col-md-12 col-lg-4">
      <grainbin-card :grainbin="grainbin" />
    </div>
    <div class="col-md-12 col-lg-8">
      <grainbin-update :grainbinID="grainbin.id" />
    </div>
  </div>
</template>

<script lang="ts" , setup>
import { onMounted, ref } from "vue";

import { GrainbinRequest } from "@/api/grainbin.api";
import { Grainbin } from "@/interfaces/grainbin.interface";
import GrainbinCard from "@/components/grainbin/GrainbinCard.vue";
import GrainbinUpdate from "@/components/grainbin/GrainbinUpdate.vue";

const grainbinAPI = new GrainbinRequest();
const grainbins = ref<Array<Grainbin>>([]);

onMounted(() => {
  grainbinAPI.getGrainbins().then((response) => {
    grainbins.value = response;
  });
});
</script>
