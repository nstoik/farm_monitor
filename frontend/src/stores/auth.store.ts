import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'

export const useAuthStore = defineStore('auth', () => {
  const refreshToken = useStorage('refreshToken', '')
  const refreshTokenExpiry = useStorage('refreshTokenExpiry', '')
  const accessToken = useStorage('accessToken', '')
  const accessTokenExpiry = useStorage('accessTokenExpiry', '')
  const isLoading = ref(false)
  const errorMessage = ref('None')

  // The buffer to expire the tokens early to account for any network latency
  const expireBuffer = 30000

  /**
   * Clears the tokens from localStorage and logs the user out.
   */
  function logout(logoutErrorMessage: string = 'None') {
    // Clear the tokens from localStorage
    refreshToken.value = ''
    refreshTokenExpiry.value = ''
    accessToken.value = ''
    accessTokenExpiry.value = ''
    errorMessage.value = logoutErrorMessage
  }

  /**
   * Checks if the access token is valid.
   * @returns {boolean} True if the access token is valid, false otherwise.
   */
  function isAccessTokenValid(): boolean {
    if (accessTokenExpiry.value === '') {
      return false
    }
    if (accessToken.value === '') {
      return false
    }

    const accessExpiresDate = Date.parse(accessTokenExpiry.value)
    // Expire the access token early to account for any network latency
    const nowDate = Date.now() + expireBuffer
    if (accessExpiresDate < nowDate) {
      return false
    }
    errorMessage.value = 'None'
    return true
  }

  /**
   * Checks if the refresh token is valid.
   * @returns {boolean} True if the refresh token is valid, false otherwise.
   */
  function isRefreshTokenValid(): boolean {
    if (refreshTokenExpiry.value === '') {
      return false
    }
    if (refreshToken.value === '') {
      return false
    }

    const refreshExpiresDate = Date.parse(refreshTokenExpiry.value)
    // Expire the access token early to account for any network latency
    const nowDate = Date.now() + expireBuffer
    if (refreshExpiresDate < nowDate) {
      return false
    }
    errorMessage.value = 'None'
    return true
  }

  return {
    accessToken,
    accessTokenExpiry,
    errorMessage,
    isAccessTokenValid,
    isLoading,
    isRefreshTokenValid,
    logout,
    refreshToken,
    refreshTokenExpiry
  }
})
