import { afterEach, beforeEach, describe, it, expect, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import axios from 'axios'

import { APIFetch, type PaginationHeader } from '../../src/api/fetch'
import { useAuthStore } from '../../src/stores/auth.store'
import { mockAuthLogin } from '../stores/auth.store.mockdata'

vi.mock('axios')

describe('APIFetch', () => {
  let apiFetch: APIFetch
  let authStore: ReturnType<typeof useAuthStore>

  beforeEach(() => {
    apiFetch = new APIFetch()
    setActivePinia(createPinia())
    authStore = useAuthStore()

    // login
    authStore.accessToken = mockAuthLogin.accessToken
    authStore.refreshToken = mockAuthLogin.refreshToken
  })

  afterEach(() => {
    authStore.logout()
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
    it('should make a GET request with the correct endpoint and headers', async () => {
      const endpoint = 'users'
      const response = { data: 'test' }
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      axios.get.mockResolvedValueOnce(response)
      const result = await apiFetch.get(endpoint)
      expect(axios.get).toHaveBeenCalledWith(endpoint, apiFetch['axiosConfig'])
      expect(result).toEqual(response)
    })

    it('should include the access token in the headers if tokenType is "Access"', async () => {
      const endpoint = 'users'
      const response = { data: 'test' }
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      axios.get.mockResolvedValueOnce(response)
      const result = await apiFetch.get(endpoint, 'Access')

      expect(apiFetch['axiosConfig'].headers).toEqual({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${mockAuthLogin.accessToken}`
      })
      expect(axios.get).toHaveBeenCalledWith(endpoint, apiFetch['axiosConfig'])
      expect(result).toEqual(response)
    })

    it('should include the refresh token in the headers if tokenType is "Refresh"', async () => {
      // login to get the access token
      const endpoint = 'users'
      const response = { data: 'test' }
      authStore.accessToken = mockAuthLogin.accessToken
      authStore.refreshToken = mockAuthLogin.refreshToken
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      axios.get.mockResolvedValueOnce(response)
      const result = await apiFetch.get(endpoint, 'Refresh')

      expect(apiFetch['axiosConfig'].headers).toEqual({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${mockAuthLogin.refreshToken}`
      })
      expect(axios.get).toHaveBeenCalledWith(endpoint, apiFetch['axiosConfig'])
      expect(result).toEqual(response)
    })
  })

  describe('getPaginate', () => {
    const page = 2
    const pageSize = 20
    const paginationHeaderResponse: PaginationHeader = {
      total: 100,
      totalPages: 5,
      firstPage: 1,
      lastPage: 5,
      page: page
    }
    const response = {
      data: new Array(20),
      headers: { 'X-Pagination': JSON.stringify(paginationHeaderResponse) }
    }

    it('should make a GET request with the correct endpoint, page, pageSize, and headers', async () => {
      const endpoint = 'users'
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      axios.get.mockResolvedValueOnce(response)
      const result = await apiFetch.getPaginate(endpoint, page, pageSize)

      expect(axios.get).toHaveBeenCalledWith(endpoint, {
        ...apiFetch['axiosConfig'],
        params: { page: page, page_size: pageSize }
      })
      expect(result).toEqual([response, paginationHeaderResponse])
    })

    it('should include the access token in the headers if tokenType is "Access"', async () => {
      const endpoint = 'users'
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      axios.get.mockResolvedValueOnce(response)
      const result = await apiFetch.getPaginate(endpoint, page, pageSize, 'Access')

      expect(apiFetch['axiosConfig'].headers).toEqual({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${mockAuthLogin.accessToken}`
      })
      expect(axios.get).toHaveBeenCalledWith(endpoint, {
        ...apiFetch['axiosConfig'],
        params: { page: page, page_size: pageSize }
      })
      expect(result).toEqual([response, paginationHeaderResponse])
    })
  })

  describe('post', () => {
    it('should make a POST request with the correct endpoint, data, and headers', async () => {
      const endpoint = 'users'
      const data = { name: 'John Doe' }
      const response = { data: 'test' }
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      axios.post.mockResolvedValueOnce(response)

      const result = await apiFetch.post(endpoint, data)

      expect(axios.post).toHaveBeenCalledWith(endpoint, data, apiFetch['axiosConfig'])
      expect(result).toEqual(response)
    })

    it('should include the access token in the headers if tokenType is "Access"', async () => {
      const endpoint = 'users'
      const data = { name: 'John Doe' }
      const response = { data: 'test' }
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      axios.post.mockResolvedValueOnce(response)

      const result = await apiFetch.post(endpoint, data, 'Access')

      expect(apiFetch['axiosConfig'].headers).toEqual({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${mockAuthLogin.accessToken}`
      })
      expect(axios.post).toHaveBeenCalledWith(endpoint, data, apiFetch['axiosConfig'])
      expect(result).toEqual(response)
    })

    it('should include the refresh token in the headers if tokenType is "Refresh"', async () => {
      const endpoint = 'users'
      const data = { name: 'John Doe' }
      const response = { data: 'test' }
      // @ts-ignore: No method 'mockResolvedValueOnce' on type
      axios.post.mockResolvedValueOnce(response)

      const result = await apiFetch.post(endpoint, data, 'Refresh')

      expect(apiFetch['axiosConfig'].headers).toEqual({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${mockAuthLogin.refreshToken}`
      })
      expect(axios.post).toHaveBeenCalledWith(endpoint, data, apiFetch['axiosConfig'])
      expect(result).toEqual(response)
    })
  })
})
