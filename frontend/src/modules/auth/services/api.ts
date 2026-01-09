import { apiClient } from '@/shared/services';
import type {
  LoginCredentials,
  RegisterData,
  TokenResponse,
  UserApiResponse,
} from '../types';

const BASE_PATH = '/api/v1/auth';

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>(
      `${BASE_PATH}/login`,
      credentials
    );
    return response.data;
  },

  register: async (data: RegisterData): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>(
      `${BASE_PATH}/register`,
      {
        email: data.email,
        password: data.password,
        display_name: data.displayName,
      }
    );
    return response.data;
  },

  getMe: async (): Promise<UserApiResponse> => {
    const response = await apiClient.get<UserApiResponse>(`${BASE_PATH}/me`);
    return response.data;
  },

  refresh: async (): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>(`${BASE_PATH}/refresh`);
    return response.data;
  },
};
