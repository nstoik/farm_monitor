import axios, { AxiosError, type AxiosInstance, type AxiosResponse } from 'axios'
import { camelizeKeys } from 'humps'

import { useAuthStore } from '@/stores/auth.store'

/**
 * Represents an authentication service.
 */
export class AuthAPI {
  private baseURL: string
  private newTokenURL: string
  private refreshTokenURL: string
  private axiosClient: AxiosInstance
  private refreshTokenTimerTimeout: number | null

  /**
   * Constructs a new instance of the AuthApi class.
   * @constructor
   */
  constructor() {
    const apiHostname: string = import.meta.env.VITE_API_HOSTNAME // eg. api.localhost
    const apiPort: string = import.meta.env.VITE_API_PORT // eg. 80
    const apiPrefix: string = import.meta.env.VITE_API_PREFIX // eg. /api
    const apiProtocol: string = import.meta.env.VITE_API_PROTOCOL || 'http' // eg. http
    const apiHTTPTimeout: number = Number(import.meta.env.VITE_API_HTTP_TIMEOUT) || 5000 // eg. 5000

    this.baseURL = `${apiProtocol}://${apiHostname}:${apiPort}${apiPrefix}/`
    this.newTokenURL = `${this.baseURL}auth/`
    this.refreshTokenURL = `${this.baseURL}auth/refresh`
    this.refreshTokenTimerTimeout = null

    this.axiosClient = axios.create({
      baseURL: this.baseURL,
      timeout: apiHTTPTimeout,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    this.axiosClient.interceptors.request.use(undefined, AuthAPI.onRequestError)
    this.axiosClient.interceptors.response.use(undefined, AuthAPI.onResponseError)
  }

  /**
   * Handles errors that occur during the request for authentication.
   * @param error - The AxiosError object representing the error.
   * @throws The error message.
   */
  private static onRequestError(error: AxiosError) {
    const authStore = useAuthStore()
    authStore.errorMessage = error.message
    console.error('Error in request for auth', error)
    throw error.message
  }

  /**
   * Handles the error response from an API request.
   * If the response status is 401, sets the error message in the auth store.
   * Otherwise, logs the error and throws it.
   * @param error - The AxiosError object representing the error response.
   */
  private static onResponseError(error: AxiosError) {
    const authStore = useAuthStore()
    if (error.response) {
      if (error.response.status === 401) {
        authStore.errorMessage = 'Invalid username or password'
        return
      }
      authStore.errorMessage = error.message
      console.error('Error in response for auth', error)
      throw error
    }
    authStore.errorMessage = error.message
  }

  /**
   * Logs in a user with the provided username and password.
   * If the access token is valid, no login attempt is made.
   * If the refresh token is valid, the access token is refreshed instead of logging in.
   * @param {string} username - The username of the user.
   * @param {string} password - The password of the user.
   * @returns {Promise<boolean>} - A promise that resolves when the login process is complete.
   */
  async login(username: string, password: string): Promise<boolean> {
    const content = {
      username,
      password
    }
    const authStore = useAuthStore()

    // if the access token is valid, do not attempt to login again
    if (authStore.isAccessTokenValid()) {
      return true
    }
    // if the refresh token is valid, refresh the access token instead of logging in
    if (authStore.isRefreshTokenValid()) {
      return await this.refresh()
    }
    // otherwise, attempt to log in
    authStore.isLoading = true
    await this.axiosClient
      .post(this.newTokenURL, content)
      .then((response: AxiosResponse) => {
        if (response && response.status === 200) {
          response.data = camelizeKeys(response.data)
          authStore.accessToken = response.data.accessToken
          authStore.accessTokenExpiry = response.data.accessExpires
          authStore.refreshToken = response.data.refreshToken
          authStore.refreshTokenExpiry = response.data.refreshExpires
          this.startRefreshTokenTimer()
          return true
        }
      })
      .finally(() => {
        authStore.isLoading = false
      })
    return false
  }

  /**
   * Refreshes the access token by sending a request to the server using the refresh token.
   * If the refresh token is expired, the user is logged out and an error message is set.
   * @returns {Promise<boolean>} A promise that resolves when the access token is successfully refreshed.
   */
  async refresh(): Promise<boolean> {
    const authStore = useAuthStore()
    const config = {
      headers: {
        'content-type': 'application/json',
        Authorization: `Bearer ${authStore.refreshToken}`
      }
    }
    if (!authStore.isRefreshTokenValid()) {
      authStore.logout('Refresh token expired. Please log in again.')
      return false
    }
    // if the access token is valid, do not attempt to refresh it again
    if (authStore.isAccessTokenValid()) {
      this.startRefreshTokenTimer()
      return true
    }
    authStore.isLoading = true
    await this.axiosClient
      .post(this.refreshTokenURL, {}, config)
      .then((response: AxiosResponse) => {
        if (response && response.status === 200) {
          response.data = camelizeKeys(response.data)
          authStore.accessToken = response.data.accessToken
          authStore.accessTokenExpiry = response.data.accessExpires
          return true
        }
      })
      .finally(() => {
        authStore.isLoading = false
        this.startRefreshTokenTimer()
      })
    return false
  }

  /**
   * Starts the refresh token timer.
   * This timer is responsible for refreshing the access token before it expires.
   * If the access token is already expired, the refresh token timer is set to 1 minute.
   */
  private startRefreshTokenTimer() {
    const authStore = useAuthStore()
    const accessExpiresDate: number = Date.parse(authStore.accessTokenExpiry)
    const nowDate = Date.now()
    // Refresh the access token 15 seconds before it expires
    let timeToRefresh = accessExpiresDate - nowDate - 15000

    // If the time to refresh is less than or equal to 0,
    // set a timeout of 1 minute to check again
    if (timeToRefresh <= 0) {
      timeToRefresh = 60000
    }

    // Cancel the refresh token timer if it is already set
    if (this.refreshTokenTimerTimeout) {
      clearTimeout(this.refreshTokenTimerTimeout)
      this.refreshTokenTimerTimeout = null
    }
    this.refreshTokenTimerTimeout = window.setTimeout(() => {
      this.refresh()
    }, timeToRefresh)
  }
}
