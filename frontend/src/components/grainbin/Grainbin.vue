<template>
  <h2>Grainbins</h2>
  <div v-if="grainbins.length == 0" class="row">
    <h3>No grainbins found</h3>
  </div>
</template>

<script lang="ts" , setup>
import { ref } from "vue";

import { Grainbin } from "@/interfaces/grainbin.interface";

const grainbins = ref<Array<Grainbin>>([]);
</script>
>
