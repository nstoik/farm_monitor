import 'bootstrap/dist/css/bootstrap.css'
import './assets/main.css'

import '@popperjs/core'
import 'bootstrap'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth.store'

const app = createApp(App)

app.use(createPinia())
app.use(router)


// attempt to auto refresh the access token before startup
try {
    const authStore = useAuthStore()
    await authStore.refresh()
} catch (error) {
    console.error('Error refreshing access token', error)
}

app.mount('#app')