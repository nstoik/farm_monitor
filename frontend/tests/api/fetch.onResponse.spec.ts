import { describe, it, expect } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

import { APIFetch } from '@/api/fetch'
import { useAuthStore } from '../../src/stores/auth.store'

describe('Axios Interceptor onResponse', () => {
  it('should convert snake_case to camelCase', () => {
    const response = {
      headers: { 'content-type': 'application/json' },
      data: {
        first_name: 'John',
        last_name: 'Doe'
      }
    }
    // @ts-ignore
    const result = APIFetch.onResponse(response)
    expect(result.data).toEqual({
      firstName: 'John',
      lastName: 'Doe'
    })
  })
  it('should convert list of data to camelCase', () => {
    const response = {
      headers: { 'content-type': 'application/json' },
      data: [
        {
          first_name: 'John',
          last_name: 'Doe'
        },
        {
          first_name: 'Jane',
          last_name: 'Doe'
        }
      ]
    }
    // @ts-ignore
    const result = APIFetch.onResponse(response)

    expect(result.data).toEqual([
      {
        firstName: 'John',
        lastName: 'Doe'
      },
      {
        firstName: 'Jane',
        lastName: 'Doe'
      }
    ])
  })
  it('should not convert data if content-type is not application/json', () => {
    const response = {
      headers: {
        'content-type': 'text/html'
      }
    }
    // @ts-ignore
    const result = APIFetch.onResponse(response)
    expect(result).toEqual(response)
  })
  it('should not convert data if response.data is undefined', () => {
    const response = {
      headers: { 'content-type': 'application/json' },
      data: undefined
    }
    // @ts-ignore
    const result = APIFetch.onResponse(response)
    expect(result).toEqual(response)
  })
  it('should not convert data if response.data is null', () => {
    const response = {
      headers: { 'content-type': 'application/json' },
      data: null
    }
    // @ts-ignore
    const result = APIFetch.onResponse(response)
    expect(result).toEqual(response)
  })
  describe('onResponseError', () => {
    it('should log out the user and display an error message if the response status is 401', () => {
      const error = {
        response: {
          status: 401
        }
      }
      setActivePinia(createPinia())
      const authStore = useAuthStore()
      // @ts-ignore
      APIFetch.onResponseError(error)
      expect(authStore.errorMessage).toBe('Invalid username or password')
    })
    it('should log out the user and display an error message if the response status is 403', () => {
      const error = {
        response: {
          status: 403
        }
      }
      setActivePinia(createPinia())
      const authStore = useAuthStore()
      // @ts-ignore
      APIFetch.onResponseError(error)
      expect(authStore.errorMessage).toBe('Invalid username or password')
    })
    it('should log the error and throw it if the response status is not 401 or 403', () => {
      const error = {
        response: {
          status: 500
        },
        message: 'Test error'
      }
      setActivePinia(createPinia())
      const authStore = useAuthStore()
      authStore.errorMessage = ''
      expect(() => {
        // @ts-ignore
        APIFetch.onResponseError(error)
      }).toThrowError(error.message)
      expect(authStore.errorMessage).toBe('Test error')
    })
  })
})
