import { afterEach, beforeEach, describe, it, expect, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

import { APIFetch } from '@/api/fetch_new'
import { useAuthStore } from '../../src/stores/auth.store'
import { mockAuthLoginSuccessResponse, mockAuthRefreshSuccessResponse } from './auth.store.mockdata'

vi.mock('@/api/fetch_new', () => {
  const APIFetch = vi.fn()
  APIFetch.prototype.post = vi.fn()
  APIFetch.prototype.get = vi.fn()

  return { APIFetch }
})

describe('Auth Store', () => {
  let authStore: ReturnType<typeof useAuthStore>
  let apiFetch: any

  beforeEach(() => {
    setActivePinia(createPinia())
    authStore = useAuthStore()
    apiFetch = new APIFetch()
    // use fake timers for the startRefreshTokenTimer function
    vi.useFakeTimers()
  })

  afterEach(() => {
    authStore.logout()
    vi.restoreAllMocks()
    vi.clearAllMocks()
  })

  it('basic state', () => {
    expect(authStore.accessToken).toBe('')
    expect(authStore.refreshToken).toBe('')
    expect(authStore.isLoading).toBeFalsy()
    expect(authStore.errorMessage).toBe('None')
  })

  it('should log in the user', async () => {
    apiFetch.post.mockResolvedValue(mockAuthLoginSuccessResponse)
    await authStore.login('username', 'password')
    expect(authStore.accessToken).toBeTruthy()
    expect(authStore.refreshToken).toBeTruthy()
  })

  it('should log out the user', () => {
    authStore.logout()
    expect(authStore.accessToken).toBeFalsy()
    expect(authStore.refreshToken).toBeFalsy()
  })

  it('should refresh the access token', async () => {
    apiFetch.post.mockResolvedValueOnce(mockAuthLoginSuccessResponse)
    await authStore.login('username', 'password')
    const oldAccessToken = authStore.accessToken
    apiFetch.post.mockResolvedValueOnce(mockAuthRefreshSuccessResponse)
    await authStore.refresh()
    expect(authStore.accessToken).not.toBe(oldAccessToken)
  })

  it('should check if the tokens are invalid if not logged in', async () => {
    authStore.logout()
    expect(authStore.isAccessTokenValid()).toBeFalsy()
    expect(authStore.isRefreshTokenValid()).toBeFalsy()
  })

  it('should check if the access token is valid', async () => {
    apiFetch.post.mockResolvedValueOnce(mockAuthLoginSuccessResponse)
    await authStore.login('username', 'password')
    // One second before the token expires (with the 30 second buffer)
    // Monday, February 19, 2024 4:07:04 AM
    const date = new Date(2024, 1, 19, 4, 6, 33)
    vi.setSystemTime(date)
    expect(authStore.isAccessTokenValid()).toBeTruthy()
  })

  it('should check if the refresh token is valid', async () => {
    apiFetch.post.mockResolvedValueOnce(mockAuthLoginSuccessResponse)
    await authStore.login('username', 'password')
    expect(authStore.isRefreshTokenValid()).toBeTruthy()
  })

  it('should check if the access token has expired', async () => {
    apiFetch.post.mockResolvedValueOnce(mockAuthLoginSuccessResponse)
    await authStore.login('username', 'password')
    // One second after the token expires
    // Monday, February 19, 2024 4:07:36 AM
    const date = new Date(2024, 1, 19, 4, 7, 36)
    vi.setSystemTime(date)
    expect(authStore.isAccessTokenValid()).toBeFalsy()
  })

  it('should check if the refresh token has expired', async () => {
    apiFetch.post.mockResolvedValueOnce(mockAuthLoginSuccessResponse)
    await authStore.login('username', 'password')
    // One second after the token expires
    // Wednesday, March 20, 2024 3:52:04 AM
    const date = new Date(2024, 2, 20, 3, 51, 36)
    vi.setSystemTime(date)
    expect(authStore.isRefreshTokenValid()).toBeFalsy()
  })
})
