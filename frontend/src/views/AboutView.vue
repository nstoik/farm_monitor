<script setup lang="ts">
import { useAuthStore } from '@/stores/auth.store'
import { useGrainbinStore } from '@/stores/grainbin.store'
import { useGrainbinUpdateStore } from '@/stores/grainbin-update.store'

const authStore = useAuthStore()
const grainbinStore = useGrainbinStore()
const grainbinUpdateStore = useGrainbinUpdateStore()

const handleLogin = (username: string, password: string) => {
  authStore.login(username, password)
}
const handleLogout = () => {
  authStore.logout()
}

const handleGetLatestGrainbinUpdates = () => {
  grainbinStore.grainbins.forEach((grainbin) => {
    grainbinUpdateStore.fetchLatestGrainbinUpdates(grainbin.id)
  })
}
</script>

<template>
  <div class="about">
    <div class="container">
      <h1>Grainbin Testing</h1>
      <button @click="grainbinStore.getGrainbinByID(1)">Get Grainbin 1</button>
      <button @click="grainbinStore.getGrainbins()">Get Grainbins</button>
      <button @click="handleGetLatestGrainbinUpdates">Get All Updates</button>
      <h1>This is an about page</h1>
      <p>AuthStore is loading: {{ authStore.isLoading }}</p>
      <p>Authstore error message: {{ authStore.errorMessage }}</p>
      <p>Authstore is access token valid: {{ authStore.isAccessTokenValid() }}</p>
      <p>Authstore is refresh token valid: {{ authStore.isRefreshTokenValid() }}</p>
      <button @click="handleLogin('admin', 'farm_monitor')">Login</button>
      <button @click="handleLogin('admin1', 'farm_monitor')">Login Wrong</button>
      <button @click="handleLogout">Logout</button>
    </div>
  </div>
</template>
