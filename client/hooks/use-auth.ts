import { INITIAL_AUTH_STATE } from "@/lib/auth";
import type { AuthState } from "@/lib/auth";

export function useAuth(): AuthState & {
  login: () => void;
  logout: () => void;
} {
  // TODO: Implement when backend auth API is ready
  return {
    ...INITIAL_AUTH_STATE,
    login: () => {},
    logout: () => {},
  };
}
