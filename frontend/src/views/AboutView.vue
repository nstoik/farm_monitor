<script setup lang="ts">
import { useAuthStore } from '@/stores/auth.store'

const authStore = useAuthStore()

const handleLogin = (username: string, password: string) => {
  authStore.login(username, password)
}
const handleLogout = () => {
  authStore.logout()
}
</script>

<template>
  <div class="about">
    <div class="container">
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
