import { useAuthStore } from '../store/authStore';

/**
 * Hook for accessing auth state and actions.
 * This is a convenience wrapper around the auth store.
 */
export function useAuth() {
  const {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    checkAuth,
  } = useAuthStore();

  return {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    checkAuth,
  };
}
