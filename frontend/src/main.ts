import 'bootstrap/dist/css/bootstrap.css'
import './assets/main.css'

import '@popperjs/core'
import 'bootstrap'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

// call the refresh method to refresh the access token.
// This will also start the process of refreshing the access token when it expires.
// import { AuthAPI } from '@/api/auth.api'
// const authAPI = new AuthAPI()
// authAPI.refresh()
