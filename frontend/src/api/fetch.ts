import axios, {
  type AxiosError,
  type AxiosInstance,
  type AxiosRequestConfig,
  type AxiosResponse,
} from "axios";
import { camelizeKeys, decamelizeKeys } from "humps";

import { AuthService } from "./auth.api";
import type { PaginationHeader } from "@/interfaces/fetch.interface";

export default abstract class Request {
  protected baseURL: string;
  protected resourceLocation: string;
  private isRefreshing: boolean;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private failedRequests: Array<{ resolve: any; reject: any }>;
  protected client: AxiosInstance;
  private authService: AuthService;

  constructor() {
    const apiHostname: string = import.meta.env.VITE_API_HOSTNAME; // eg. api.localhost
    const apiPort: string = import.meta.env.VITE_API_PORT; // eg. 80
    const apiPrefix: string = import.meta.env.VITE_API_PREFIX; // eg. /api
    const apiProtocol: string = import.meta.env.VITE_API_PROTOCOL || "http"; // eg. http
    const apiHTTPTimeout: number =
      Number(import.meta.env.VITE_API_HTTP_TIMEOUT) || 5000; // eg. 5000

    this.baseURL = `${apiProtocol}://${apiHostname}:${apiPort}${apiPrefix}/`;
    this.isRefreshing = false;
    this.failedRequests = [];
    this.authService = new AuthService();
    this.client = axios.create({ timeout: apiHTTPTimeout });
    this.resourceLocation = this.baseURL;

    this.client.interceptors.request.use(
      Request.onRequest,
      Request.onRequestError
    );
    this.client.interceptors.response.use(
      Request.onResponse,
      this.onResponseError.bind(this)
    );

    // Convert responses and requests between camelCase and snake_case
    this.client.interceptors.response.use(Request.convertToCamelCase);
    this.client.interceptors.request.use(Request.convertToSnakeCase);
  }

  /**
   * A public function to get a resource type from the
   * server.
   * @param url: the url to the resource. eg: `${this.resourceLocation}/paginate`
   * @param params: optional. the parameters to send to the server.
   *
   * @returns An array of two items. The first item is an array
   * of the returned resources. The second is a pagination header
   * object detailing the current status of the return.
   */
  public getPaginate<T>(
    url: string,
    page = 1,
    pageSize = 10
  ): Promise<[Array<T>, PaginationHeader]> {
    const params = { page: page, page_size: pageSize };
    return this.client
      .get<Array<T>>(url, { params: params })
      .then((response) => {
        const paginationHeader: PaginationHeader = JSON.parse(
          response.headers["x-pagination"]
        );
        camelizeKeys(paginationHeader);
        return [response.data, paginationHeader];
      });
  }

  /**
   * Convert incoming api responses to camelCase.
   *
   * @param response the incoming AxiosResponse
   * @returns the updated AxiosResponse
   */
  private static convertToCamelCase(response: AxiosResponse): AxiosResponse {
    if (
      response.data &&
      response.headers["content-type"] === "application/json"
    ) {
      response.data = camelizeKeys(response.data);
    }
    return response;
  }

  /**
   * Convert outgoing api requests to snake_case
   * @param config the outgoing AxiosRequestConfig
   * @returns the updated AxiosRequestConfig
   */
  private static convertToSnakeCase(
    config: AxiosRequestConfig
  ): AxiosRequestConfig {
    const newConfig = { ...config };

    if (newConfig.headers) {
      if (newConfig.headers["Content-Type"] === "multipart/form-data") {
        return newConfig;
      }
    }
    if (config.params) {
      newConfig.params = decamelizeKeys(config.params);
    }
    if (config.data) {
      newConfig.data = decamelizeKeys(config.data);
    }
    return newConfig;
  }

  private static onRequest(config: AxiosRequestConfig): AxiosRequestConfig {
    // At this point, no authorization is being used, so we can skip this step.
    // November 12, 2021.
    //
    // // Add the authorization token to every request
    // const token = `Bearer ${AuthService.getAccessToken()}`;
    // config.headers["Content-Type"] = "application/json";
    // config.headers.Authorization = token;
    return config;
  }

  private static onRequestError(error: AxiosError): Promise<AxiosError> {
    console.error(`[request error] [${JSON.stringify(error)}]`);
    return Promise.reject(error);
  }

  private static onResponse(response: AxiosResponse): AxiosResponse {
    return response;
  }

  private async onResponseError(error: AxiosError): Promise<AxiosError> {
    const responseStatus = error.response?.status;
    const responseMessage = error.response?.data.msg;
    if (responseStatus === 401 && responseMessage === "Token has expired") {
      return this.handleUnauthorized(error);
    } else if (error.message.startsWith("timeout of ")) {
      throw "Server Timeout";
    }
    console.error(`[unknown response error] [${JSON.stringify(error)}]`);

    return Promise.reject(error);
  }

  private async handleUnauthorized(error: AxiosError): Promise<AxiosError> {
    if (this.isRefreshing) {
      try {
        // the request failed and the token is being refreshed. Wait for the token to be refreshed.
        await new Promise<void>((resolve, reject) => {
          this.failedRequests.push({ resolve, reject });
        });
        // Now try the same request again after the token has been refreshed.
        return this.client.request(error.config);
      } catch (anotherError) {
        console.warn(
          `Error while waiting for token being refreshed: ${anotherError}`
        );
        return Promise.reject(anotherError);
      }
    }
    this.isRefreshing = true;
    await this.authService.fetchNewAccessToken();
    this.isRefreshing = false;
    this.proccesQueue();
    return this.client.request(error.config);
  }

  /**
   * Called once the token has been refreshed.
   * Resolve all promises that were queued so those requests can be tried again.
   */
  private proccesQueue() {
    this.failedRequests.forEach((promise) => {
      promise.resolve();
    });
    this.failedRequests = [];
  }
}
