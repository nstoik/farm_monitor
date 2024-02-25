import axios, {
  type AxiosError,
  type AxiosRequestConfig,
  type AxiosResponse,
  type InternalAxiosRequestConfig
} from 'axios'
import { snakeCase, camelCase } from 'change-case'

import { useAuthStore } from '@/stores/auth.store'

/**
 * Represents a pagination header returned by the API.
 */
export type PaginationHeader = {
  total: number
  totalPages: number
  firstPage: number
  lastPage: number
  page: number
}

export class APIFetch {
  private baseURL: string
  private axiosConfig: AxiosRequestConfig

  /**
   * Constructs a new instance of the APIFetch class.
   * @constructor
   */
  constructor() {
    const apiHostname: string = import.meta.env.VITE_API_HOSTNAME // eg. api.localhost
    const apiPort: string = import.meta.env.VITE_API_PORT // eg. 80
    const apiPrefix: string = import.meta.env.VITE_API_PREFIX // eg. /api
    const apiProtocol: string = import.meta.env.VITE_API_PROTOCOL || 'http' // eg. http
    const apiHTTPTimeout: number = Number(import.meta.env.VITE_API_HTTP_TIMEOUT) || 5000 // eg. 5000

    this.baseURL = `${apiProtocol}://${apiHostname}:${apiPort}${apiPrefix}/`
    this.axiosConfig = {
      baseURL: this.baseURL,
      timeout: apiHTTPTimeout,
      headers: {
        'Content-Type': 'application/json'
      }
    }
    axios.interceptors.request.use(APIFetch.onRequest, APIFetch.onRequestError)
    axios.interceptors.response.use(APIFetch.onResponse, APIFetch.onResponseError)
  }

  /**
   * Retrieves data from the specified endpoint.
   *
   * @template T - The type of data to be retrieved.
   * @param {string} endpoint - The endpoint to fetch the data from.
   * @param {'Access' | 'Refresh'} [tokenType] - The type of token to be used for authentication.
   * @returns {Promise<AxiosResponse<T>>} - A promise that resolves to the Axios response.
   */
  public async get<T>(
    endpoint: string,
    tokenType?: 'Access' | 'Refresh'
  ): Promise<AxiosResponse<T>> {
    if (tokenType) {
      this.authHeaderHelper(tokenType)
    }
    return axios.get<T>(endpoint, this.axiosConfig)
  }

  /**
   * Retrieves paginated data from the specified endpoint.
   *
   * @template T - The type of data to be retrieved.
   * @param {string} endpoint - The endpoint to fetch the data from.
   * @param {number} [page=1] - The page number to retrieve (default: 1).
   * @param {number} [pageSize=10] - The number of items per page (default: 10).
   * @param {'Access' | 'Refresh'} [tokenType] - The type of token to be used for authentication.
   * @returns {Promise<[AxiosResponse<T[]>, PaginationHeader]>} - A promise that resolves to an array containing the Axios response and the pagination header.
   */
  public async getPaginate<T>(
    endpoint: string,
    page: number = 1,
    pageSize: number = 10,
    tokenType?: 'Access' | 'Refresh'
  ): Promise<[AxiosResponse<T[]>, PaginationHeader]> {
    if (tokenType) {
      this.authHeaderHelper(tokenType)
    }
    // add params to the axiosConfig
    this.axiosConfig.params = { page, page_size: pageSize }
    return axios.get<Array<T>>(endpoint, this.axiosConfig).then((response) => {
      const paginationHeader: PaginationHeader = JSON.parse(response.headers['X-Pagination'])
      return [response, paginationHeader]
    })
  }

  /**
   * Sends a POST request to the specified endpoint with the provided data.
   *
   * @template T - The type of the response data.
   * @param {string} endpoint - The endpoint to send the request to.
   * @param {any} data - The data to send with the request.
   * @param {'Access' | 'Refresh'} [tokenType] - The type of token to include in the request header.
   * @returns {Promise<AxiosResponse<T>>} - A promise that resolves to the response data.
   */
  public async post<T>(
    endpoint: string,
    data: any,
    tokenType?: 'Access' | 'Refresh'
  ): Promise<AxiosResponse<T>> {
    if (tokenType) {
      this.authHeaderHelper(tokenType)
    }
    return axios.post<T>(endpoint, data, this.axiosConfig)
  }

  /**
   * Sets the Authorization header in the axios configuration object based on the token type.
   * @param {'Access' | 'Refresh'} [tokenType] - The type of token ('Access' or 'Refresh').
   * @returns {void}
   */
  private authHeaderHelper(tokenType: 'Access' | 'Refresh'): void {
    const authStore = useAuthStore()
    let token = ''

    if (tokenType === 'Refresh') {
      token = authStore.refreshToken
    }
    if (tokenType === 'Access') {
      token = authStore.accessToken
    }

    if (this.axiosConfig.headers) {
      this.axiosConfig.headers['Authorization'] = `Bearer ${token}`
    } else {
      this.axiosConfig.headers = {
        Authorization: `Bearer ${token}`
      }
    }
    return
  }
  /**
   * Modifies the Axios request configuration before sending the request.
   * Converts outgoing API requests to snake_case.
   * @param config - The Axios request configuration.
   * @returns The modified Axios request configuration.
   */
  private static onRequest(config: InternalAxiosRequestConfig): InternalAxiosRequestConfig {
    // Convert outgoing api requests to snake_case
    if (config.headers) {
      if (config.headers['Content-Type'] === 'multipart/form-data') {
        return config
      }
    }
    if (config.params) {
      config.params = Object.keys(config.params).reduce((acc: { [key: string]: any }, key) => {
        const snakeCaseKey = snakeCase(key)
        acc[snakeCaseKey] = config.params[key]
        return acc
      }, {})
    }
    if (config.data) {
      // if config.data is an array, convert each object in the array to snake_case
      if (Array.isArray(config.data)) {
        config.data = config.data.map((item) => APIFetch.convertToSnakeCase(item))
      } else {
        config.data = APIFetch.convertToSnakeCase(config.data)
      }
    }
    return config
  }

  /**
   * Handles the error that occurs during a request.
   * @param error - The AxiosError object representing the error.
   * @throws The original error object.
   */
  private static onRequestError(error: AxiosError) {
    const authStore = useAuthStore()
    console.error('Error in request', error)
    authStore.errorMessage = error.message
    throw error
  }

  /**
   * Converts the incoming API response to camelCase.
   * @param response - The AxiosResponse object representing the API response.
   * @returns The modified AxiosResponse object with camelCased data.
   */
  private static onResponse(response: AxiosResponse): AxiosResponse {
    // Convert incoming api responses to camelCase.
    if (response && response.data && response.headers['content-type'] === 'application/json') {
      if (Array.isArray(response.data)) {
        response.data = response.data.map((item) => APIFetch.convertToCamelCase(item))
      } else {
        response.data = APIFetch.convertToCamelCase(response.data)
      }
    }
    return response
  }

  /**
   * Handles the error response from an API request.
   * If the response status is 401 or 403, it logs out the user and displays an error message.
   * Otherwise, it logs the error and throws it.
   * @param error - The AxiosError object representing the error response.
   */
  private static onResponseError(error: AxiosError) {
    const authStore = useAuthStore()
    if (error.response) {
      // Handle 401 and 403 errors
      if ([401, 403].includes(error.response.status)) {
        authStore.logout('Invalid username or password')
        return
      }
    }
    console.error('Error in response', error)
    authStore.errorMessage = error.message
    throw error
  }

  /**
   * Converts an object to snake_case.
   * @param obj - The object to convert.
   * @returns The converted object with snake_cased keys.
   */
  private static convertToSnakeCase(obj: { [key: string]: any }): { [key: string]: any } {
    return Object.keys(obj).reduce((acc: { [key: string]: any }, key) => {
      const snakeCaseKey = snakeCase(key)
      acc[snakeCaseKey] = obj[key]
      return acc
    }, {})
  }

  /**
   * Converts the keys of an object to camel case.
   * @param obj - The object to convert.
   * @returns The object with camel case keys.
   */
  private static convertToCamelCase(obj: { [key: string]: any }): { [key: string]: any } {
    return Object.keys(obj).reduce((acc: { [key: string]: any }, key) => {
      const camelCaseKey = camelCase(key)
      acc[camelCaseKey] = obj[key]
      return acc
    }, {})
  }
}
