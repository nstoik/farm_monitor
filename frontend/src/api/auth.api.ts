import axios, { AxiosError, AxiosInstance } from "axios";

/**
 * AuthService is used to get delete and retrieve access and refresh
 * tokens from the server.
 */
export class AuthService {
  private baseURL: string;
  private newTokenURL: string;
  private refreshTokenURL: string;
  private axiosClient: AxiosInstance;

  constructor() {
    const apiHostname: string = import.meta.env.VITE_API_HOSTNAME; // eg. api.localhost
    const apiPort: string = import.meta.env.VITE_API_PORT; // eg. 80
    const apiPrefix: string = import.meta.env.VITE_API_PREFIX; // eg. /api
    const apiProtocol: string = import.meta.env.VITE_API_PROTOCOL || "http"; // eg. http
    const apiHTTPTimeout: number =
      Number(import.meta.env.VITE_API_HTTP_TIMEOUT) || 5000; // eg. 5000

    this.baseURL = `${apiProtocol}://${apiHostname}:${apiPort}${apiPrefix}/`;
    this.newTokenURL = `${this.baseURL}auth/`;
    this.refreshTokenURL = `${this.baseURL}auth/refresh`;

    this.axiosClient = axios.create({ timeout: apiHTTPTimeout });

    this.axiosClient.interceptors.request.use(
      undefined,
      AuthService.onRequestError
    );
    this.axiosClient.interceptors.response.use(
      undefined,
      AuthService.onResponseError
    );
  }

  private static onRequestError(error: AxiosError) {
    console.error("Error in request for auth", error);
    throw error.message;
  }

  private static onResponseError(error: AxiosError) {
    if (error.message.startsWith("timeout of ")) {
      throw "Server Timeout";
    }
    if (error.response) {
      // Request made and server responded
      if (error.response.status === 422) {
        const usernameError: string =
          error.response.data?.errors?.json?.username?.[0];
        if (usernameError) {
          throw "Username: " + usernameError;
        }
        const passwordError: string =
          error.response.data?.errors?.json?.password?.[0];
        if (passwordError) {
          throw "Password: " + passwordError;
        }
      }
      throw error.response.data.message;
    } else if (error.request) {
      throw error.message;
    } // The request was made but no response was received
    // Something happened in setting up the request that triggered an Error
    throw error;
  }

  /**
   * Check if the access token is valid or expired
   * @returns: boolean - If the access token is valid or not
   */
  public static checkAccessTokenValidity(): boolean {
    const accessExpires = localStorage.getItem("accessExpires");
    const accessToken = localStorage.getItem("accessToken");

    if (accessExpires !== null && accessToken !== null) {
      const accessExpiresDate = Date.parse(accessExpires);
      const nowDate = Date.now();
      if (accessExpiresDate <= nowDate) {
        return false;
      }
      return true;
    }
    return false;
  }

  /**
   * Check if the refresh token is valid or expired
   * @returns: boolean - If the refresh token is valid or not
   */
  public static checkRefreshTokenValidity(): boolean {
    const refreshExpires = localStorage.getItem("refreshExpires");
    const refreshToken = localStorage.getItem("refreshToken");

    if (refreshExpires !== null && refreshToken !== null) {
      const accessExpiresDate = Date.parse(refreshToken);
      const nowDate = Date.now();
      if (accessExpiresDate >= nowDate) {
        return false;
      }
      return true;
    }
    return false;
  }

  /**
   * Get the access token if it is stored in localStorage
   * @returns: string - The access token or null
   */
  public static getAccessToken(): string | null {
    const accessToken = localStorage.getItem("accessToken");

    if (accessToken === null) {
      return null;
    }
    return accessToken;
  }

  /**
   * Get the refresh token if it is stored in localStorage
   * @returns: string - The refresh token or null
   */
  private static getRefreshToken(): string | null {
    const refreshToken = localStorage.getItem("refreshToken");

    if (refreshToken === null) {
      return null;
    }
    return refreshToken;
  }

  /**
   * Get access and refresh tokens from the server.
   * Store the result in localStorage.
   */
  public async fetchNewTokens(
    username: string,
    password: string
  ): Promise<boolean> {
    const content = {
      username,
      password,
    };
    const url = this.newTokenURL;
    const config = {
      headers: {
        "content-type": "application/json",
      },
    };
    const response = await this.axiosClient.post(url, content, config);
    localStorage.setItem("refreshToken", response.data.refresh_token);
    localStorage.setItem("refreshExpires", response.data.refresh_expires);
    localStorage.setItem("accessToken", response.data.access_token);
    localStorage.setItem("accessExpires", response.data.access_expires);
    return true;
  }

  public static removeTokens(): void {
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("refreshExpires");
    localStorage.removeItem("accessToken");
    localStorage.removeItem("accessExpires");
  }

  /**
   * Gets a new access token from the server using the refresh token.
   */
  public async fetchNewAccessToken(): Promise<void> {
    const url = this.refreshTokenURL;
    const config = {
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${AuthService.getRefreshToken()}`,
      },
    };
    if (!AuthService.checkRefreshTokenValidity()) {
      throw new Error(
        "Refresh token has expired. You will need to log in again."
      );
    }
    const response = await this.axiosClient.post(url, {}, config);
    localStorage.setItem("accessToken", response.data.access_token);
    localStorage.setItem("accessExpires", response.data.access_expires);
  }
}

export default new AuthService();
