import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';
import type { ApiResponse, ApiError } from '@/types';

class ApiClient {
  private client: AxiosInstance;
  private baseURL: string;

  constructor() {
    this.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        // Add auth token if available
        const token = localStorage.getItem('auth_token');
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        
        // Add request timestamp
        config.headers['X-Request-Time'] = Date.now().toString();
        
        return config;
      },
      (error: AxiosError) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        return response;
      },
      async (error: AxiosError<ApiError>) => {
        if (error.response) {
          // Server responded with error
          const apiError: ApiError = {
            code: error.response.data?.code || error.response.status.toString(),
            message: error.response.data?.message || error.message,
            details: error.response.data?.details,
            timestamp: Date.now(),
          };

          // Handle specific error codes
          if (error.response.status === 401) {
            // Unauthorized - clear token and redirect to login
            localStorage.removeItem('auth_token');
            window.location.href = '/login';
          } else if (error.response.status === 429) {
            // Rate limit - implement retry with backoff
            console.warn('Rate limit hit, implementing backoff...');
          }

          return Promise.reject(apiError);
        } else if (error.request) {
          // Request made but no response
          const apiError: ApiError = {
            code: 'NETWORK_ERROR',
            message: 'Network error - please check your connection',
            timestamp: Date.now(),
          };
          return Promise.reject(apiError);
        } else {
          // Request setup error
          const apiError: ApiError = {
            code: 'REQUEST_ERROR',
            message: error.message,
            timestamp: Date.now(),
          };
          return Promise.reject(apiError);
        }
      }
    );
  }

  // Generic GET request
  async get<T>(url: string, params?: Record<string, unknown>): Promise<ApiResponse<T>> {
    const response = await this.client.get<ApiResponse<T>>(url, { params });
    return response.data;
  }

  // Generic POST request
  async post<T, D = unknown>(url: string, data?: D): Promise<ApiResponse<T>> {
    const response = await this.client.post<ApiResponse<T>>(url, data);
    return response.data;
  }

  // Generic PUT request
  async put<T, D = unknown>(url: string, data?: D): Promise<ApiResponse<T>> {
    const response = await this.client.put<ApiResponse<T>>(url, data);
    return response.data;
  }

  // Generic DELETE request
  async delete<T>(url: string): Promise<ApiResponse<T>> {
    const response = await this.client.delete<ApiResponse<T>>(url);
    return response.data;
  }

  // Generic PATCH request
  async patch<T, D = unknown>(url: string, data?: D): Promise<ApiResponse<T>> {
    const response = await this.client.patch<ApiResponse<T>>(url, data);
    return response.data;
  }

  // Get base URL
  getBaseURL(): string {
    return this.baseURL;
  }

  // Set auth token
  setAuthToken(token: string): void {
    localStorage.setItem('auth_token', token);
  }

  // Clear auth token
  clearAuthToken(): void {
    localStorage.removeItem('auth_token');
  }
}

// Export singleton instance
export const apiClient = new ApiClient();
