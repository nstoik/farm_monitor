import { afterEach, beforeEach, describe, it, expect, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import axios from 'axios'

import { APIFetch } from '../../src/api/fetch_new'
import { useAuthStore } from '../../src/stores/auth.store'
import { mockAuthLogin } from '../stores/auth.store.mockdata'

vi.mock('axios')

describe('APIFetch', () => {
  let apiFetch: APIFetch

  beforeEach(() => {
    apiFetch = new APIFetch()
  })

  afterEach(() => {
    vi.resetAllMocks()
  })

  it('should set the base URL and axios config correctly', () => {
    expect(apiFetch['baseURL']).toBe('http://localhost:5000/api/')
    expect(apiFetch['axiosConfig']).toEqual({
      baseURL: 'http://localhost:5000/api/',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    })
  })

  describe('get', () => {
    let authStore: ReturnType<typeof useAuthStore>

    beforeEach(() => {
      setActivePinia(createPinia())
      authStore = useAuthStore()

      // login
      authStore.accessToken = mockAuthLogin.accessToken
      authStore.refreshToken = mockAuthLogin.refreshToken
    })

    afterEach(() => {
      authStore.logout()
    })

    it('should make a GET request with the correct URL and headers', async () => {
      const url = 'http://localhost:5000/api/users'
      const response = { data: 'test' }
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      axios.get.mockResolvedValueOnce(response)
      const result = await apiFetch.get(url)
      expect(axios.get).toHaveBeenCalledWith(url, apiFetch['axiosConfig'])
      expect(result).toEqual(response)
    })

    it('should include the access token in the headers if tokenType is "Access"', async () => {
      const url = 'http://localhost:5000/api/users'
      const response = { data: 'test' }
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      axios.get.mockResolvedValueOnce(response)
      const result = await apiFetch.get(url, 'Access')

      expect(apiFetch['axiosConfig'].headers).toEqual({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${mockAuthLogin.accessToken}`
      })
      expect(axios.get).toHaveBeenCalledWith(url, apiFetch['axiosConfig'])
      expect(result).toEqual(response)
    })

    it('should include the refresh token in the headers if tokenType is "Refresh"', async () => {
      // login to get the access token
      const url = 'http://localhost:5000/api/users'
      const response = { data: 'test' }
      authStore.accessToken = mockAuthLogin.accessToken
      authStore.refreshToken = mockAuthLogin.refreshToken
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      axios.get.mockResolvedValueOnce(response)
      const result = await apiFetch.get(url, 'Refresh')

      expect(apiFetch['axiosConfig'].headers).toEqual({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${mockAuthLogin.refreshToken}`
      })
      expect(axios.get).toHaveBeenCalledWith(url, apiFetch['axiosConfig'])
      expect(result).toEqual(response)
    })
  })

  describe('post', () => {
    let authStore: ReturnType<typeof useAuthStore>

    beforeEach(() => {
      setActivePinia(createPinia())
      authStore = useAuthStore()

      // login
      authStore.accessToken = mockAuthLogin.accessToken
      authStore.refreshToken = mockAuthLogin.refreshToken
    })

    afterEach(() => {
      authStore.logout()
    })

    it('should make a POST request with the correct URL, data, and headers', async () => {
      const url = 'http://localhost:5000/api/users'
      const data = { name: 'John Doe' }
      const response = { data: 'test' }
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      axios.post.mockResolvedValueOnce(response)

      const result = await apiFetch.post(url, data)

      expect(axios.post).toHaveBeenCalledWith(url, data, apiFetch['axiosConfig'])
      expect(result).toEqual(response)
    })

    it('should include the access token in the headers if tokenType is "Access"', async () => {
      const url = 'http://localhost:5000/api/users'
      const data = { name: 'John Doe' }
      const response = { data: 'test' }
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      axios.post.mockResolvedValueOnce(response)

      const result = await apiFetch.post(url, data, 'Access')

      expect(apiFetch['axiosConfig'].headers).toEqual({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${mockAuthLogin.accessToken}`
      })
      expect(axios.post).toHaveBeenCalledWith(url, data, apiFetch['axiosConfig'])
      expect(result).toEqual(response)
    })

    it('should include the refresh token in the headers if tokenType is "Refresh"', async () => {
      const url = 'http://localhost:5000/api/users'
      const data = { name: 'John Doe' }
      const response = { data: 'test' }
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      axios.post.mockResolvedValueOnce(response)

      const result = await apiFetch.post(url, data, 'Refresh')

      expect(apiFetch['axiosConfig'].headers).toEqual({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${mockAuthLogin.refreshToken}`
      })
      expect(axios.post).toHaveBeenCalledWith(url, data, apiFetch['axiosConfig'])
      expect(result).toEqual(response)
    })
  })
})
