import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'

import { APIFetch } from '@/api/fetch'

export const useAuthStore = defineStore('auth', () => {
  const refreshToken = useStorage('refreshToken', '')
  const accessToken = useStorage('accessToken', '')
  const isLoading = ref(false)
  const errorMessage = ref('None')

  const refreshTokenTimeout = ref(0)
  // The buffer to expire the tokens early to account for any network latency
  const expireBuffer = 30000

  /**
   * Logs in the user with the provided username and password.
   * @param {string} username - The username of the user.
   * @param {string} password - The password of the user.
   * @returns {Promise<void>} - A promise that resolves when the login process is complete.
   */
  async function login(username: string, password: string): Promise<void> {
    // If the access token is valid, no login attempt is made
    if (isAccessTokenValid()) {
      return
    }
    isLoading.value = true
    const apiFetch = new APIFetch()
    return apiFetch
      .post('auth/jwt/', { username: username, password: password })
      .then((response) => {
        if (response && response.status === 200) {
          accessToken.value = response.data.accessToken
          refreshToken.value = response.data.refreshToken
          startRefreshTokenTimer()
        }
      })
      .finally(() => {
        isLoading.value = false
      })
  }

  /**
   * Logs out the user and clears the tokens from localStorage.
   * @param logoutErrorMessage - The error message to display upon logout. Default is 'None'.
   */
  function logout(logoutErrorMessage: string = 'None') {
    // Clear the tokens from localStorage
    refreshToken.value = ''
    accessToken.value = ''
    errorMessage.value = logoutErrorMessage
    stopRefreshTokenTimer()
  }

  /**
   * Refreshes the access token if the refresh token is valid.
   * If the refresh token is valid, it sends a POST request to 'auth/jwt/refresh' endpoint
   * to obtain a new access token. If the request is successful, it updates the access token
   * and starts the refresh token timer.
   */
  async function refresh() {
    if (isRefreshTokenValid()) {
      const apiFetch = new APIFetch()
      return apiFetch.post('auth/jwt/refresh', {}, 'Refresh').then((response) => {
        if (response && response.status === 200) {
          accessToken.value = response.data.accessToken
          startRefreshTokenTimer()
        }
      })
    }
  }

  /**
   * Starts the refresh token timer.
   * This function parses the JSON object from the base64 encoded JWT token,
   * sets a timeout to refresh the token before it expires.
   */
  function startRefreshTokenTimer() {
    // Parse json object from base64 encoded jwt token
    const jwtToken = JSON.parse(atob(accessToken.value.split('.')[1]))
    // Set a timeout to refresh the token before it expires
    const expires = new Date(jwtToken.exp * 1000)
    const timeout = expires.getTime() - Date.now() - expireBuffer
    refreshTokenTimeout.value = window.setTimeout(refresh, timeout)
  }

  /**
   * Stops the refresh token timer.
   */
  function stopRefreshTokenTimer() {
    clearTimeout(refreshTokenTimeout.value)
  }

  /**
   * Checks if the access token is valid.
   * @returns {boolean} True if the access token is valid, false otherwise.
   */
  function isAccessTokenValid(): boolean {
    if (accessToken.value === '') {
      return false
    }
    // Parse json object from base64 encoded jwt token
    const jwtToken = JSON.parse(atob(accessToken.value.split('.')[1]))
    const expires = new Date(jwtToken.exp * 1000)

    if (expires.getTime() - Date.now() - expireBuffer <= 0) {
      errorMessage.value = 'Access token expired.'
      return false
    }
    return true
  }

  /**
   * Checks if the refresh token is valid. If the refresh token is expired, it logs out the user.
   * @returns {boolean} True if the refresh token is valid, false otherwise.
   */
  function isRefreshTokenValid(): boolean {
    if (refreshToken.value === '') {
      return false
    }
    // Parse json object from base64 encoded jwt token
    const jwtToken = JSON.parse(atob(refreshToken.value.split('.')[1]))
    const expires = new Date(jwtToken.exp * 1000)

    if (expires.getTime() - Date.now() - expireBuffer <= 0) {
      logout('Refresh token expired. Please log in again.')
      return false
    }
    return true
  }

  return {
    accessToken,
    errorMessage,
    isAccessTokenValid,
    isLoading,
    isRefreshTokenValid,
    logout,
    login,
    refreshToken,
    refresh
  }
})
