import { describe, it, expect } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

import { APIFetch } from '@/api/fetch'
import { useAuthStore } from '../../src/stores/auth.store'

describe('Axios Interceptor onRequest', () => {
  it('should convert params to snake_case', () => {
    const config = {
      params: {
        firstName: 'John',
        lastName: 'Doe'
      }
    }

    //@ts-ignore
    const result = APIFetch['onRequest'](config)

    expect(result.params).toEqual({
      first_name: 'John',
      last_name: 'Doe'
    })
  })

  it('should convert data to snake_case', () => {
    const config = {
      data: {
        firstName: 'John',
        lastName: 'Doe'
      }
    }
    //@ts-ignore
    const result = APIFetch.onRequest(config)

    expect(result.data).toEqual({
      first_name: 'John',
      last_name: 'Doe'
    })
  })

  it('should convert list of data to snake_case', () => {
    const config = {
      data: [
        {
          firstName: 'John',
          lastName: 'Doe'
        },
        {
          firstName: 'Jane',
          lastName: 'Doe'
        }
      ]
    }
    //@ts-ignore
    const result = APIFetch.onRequest(config)

    expect(result.data).toEqual([
      {
        first_name: 'John',
        last_name: 'Doe'
      },
      {
        first_name: 'Jane',
        last_name: 'Doe'
      }
    ])
  })

  it('should not modify config if Content-Type is multipart/form-data', () => {
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      params: {
        firstName: 'John',
        lastName: 'Doe'
      },
      data: {
        firstName: 'John',
        lastName: 'Doe'
      }
    }

    //@ts-ignore
    const result = APIFetch.onRequest(config)

    expect(result).toEqual(config)
  })

  it('should not modify config if headers are not present', () => {
    const config = {
      params: {
        firstName: 'John',
        lastName: 'Doe'
      },
      data: {
        firstName: 'John',
        lastName: 'Doe'
      }
    }

    //@ts-ignore
    const result = APIFetch.onRequest(config)

    expect(result).toEqual(config)
  })

  describe('onRequestError', () => {
    it('should set the error message in the auth store and throw the error', () => {
      const error = new Error('Test error')
      setActivePinia(createPinia())
      const authStore = useAuthStore()
      authStore.errorMessage = ''

      expect(() => {
        //@ts-ignore
        APIFetch.onRequestError(error)
      }).toThrow(error)
      expect(authStore.errorMessage).toBe('Test error')
    })
  })
})
