"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { ROLE_DASHBOARD, clearSessionRole, setSessionRole } from "@/lib/session";
import { getErrorMessage, showErrorToast } from "@/lib/toast";
import type { AuthUser, LoginCredentials, SignupCredentials } from "@/types/auth";

export function useAuth() {
  const router = useRouter();
  const queryClient = useQueryClient();

  const { data: user, isLoading } = useQuery<AuthUser | null>({
    queryKey: ["auth", "me"],
    queryFn: async () => {
      try {
        const me = await apiFetch<AuthUser>("/auth/me");
        setSessionRole(me.role);
        return me;
      } catch {
        clearSessionRole();
        return null;
      }
    },
    retry: false,
  });

  const loginMutation = useMutation({
    mutationFn: (credentials: LoginCredentials) =>
      apiFetch<AuthUser>("/auth/login", {
        method: "POST",
        body: JSON.stringify(credentials),
      }),
    onSuccess: (data) => {
      queryClient.setQueryData(["auth", "me"], data);
      setSessionRole(data.role);
      router.push(ROLE_DASHBOARD[data.role] ?? "/");
    },
    onError: (error) => {
      showErrorToast({
        title: "Login failed",
        description: getErrorMessage(error, "Invalid credentials"),
      });
    },
  });

  const signupMutation = useMutation({
    mutationFn: (credentials: SignupCredentials) =>
      apiFetch<AuthUser>("/auth/signup", {
        method: "POST",
        body: JSON.stringify(credentials),
      }),
    onSuccess: (data) => {
      queryClient.setQueryData(["auth", "me"], data);
      setSessionRole(data.role);
      router.push(ROLE_DASHBOARD[data.role] ?? "/admin/dashboard");
    },
    onError: (error) => {
      showErrorToast({
        title: "Signup failed",
        description: getErrorMessage(error, "Could not create account"),
      });
    },
  });

  const logout = async () => {
    await apiFetch("/auth/logout", { method: "POST" }).catch(() => {});
    queryClient.setQueryData(["auth", "me"], null);
    queryClient.clear();
    clearSessionRole();
    router.push("/login");
  };

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    login: loginMutation.mutate,
    signup: signupMutation.mutate,
    logout,
    loginError: loginMutation.error,
    signupError: signupMutation.error,
    isLoggingIn: loginMutation.isPending,
    isSigningUp: signupMutation.isPending,
  };
}
