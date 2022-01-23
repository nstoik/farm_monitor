<template>
  <button
    @click="refreshApp"
    v-if="updateExists"
    type="button"
    class="btn btn-success"
  >
    Update App
  </button>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";

const registration = ref();
const updateExists = ref(false);
let refreshing = false;

interface swUpdatedEvent extends Event {
  detail?: {
    registration: ServiceWorkerRegistration;
  };
}
onMounted(() => {
  // Listen for our custom event from the SW registration.
  document.addEventListener("swUpdated", updateAvailable, { once: true });

  // Prevent multiple refreshes
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (refreshing) {
      return;
    }
    refreshing = true;
    // The actual reload of the page occurs here.
    window.location.reload();
  });
});

function updateAvailable(event: swUpdatedEvent) {
  registration.value = event.detail;
  updateExists.value = true;
}

function refreshApp() {
  updateExists.value = false;
  // Make sure we only send a 'skip waiting' message if the SW is waiting
  if (!registration.value || !registration.value.waiting) {
    return;
  }
  // Send message to SW to skip the waiting and activate the new SW
  registration.value.waiting.postMessage({ type: "SKIP_WAITING" });
}
</script>
