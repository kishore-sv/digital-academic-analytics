import { toast } from "@/components/ui/toast";
import { ApiError } from "@/lib/api";

type ToastOptions = {
  title?: string;
  description: string;
};

export function getErrorMessage(
  error: unknown,
  fallback = "Something went wrong",
) {
  if (error instanceof ApiError) return error.message;
  if (error instanceof Error) return error.message;
  return fallback;
}

export function showErrorToast({ title = "Error", description }: ToastOptions) {
  toast.add({ title, description, type: "error" });
}

export function showSuccessToast({ title = "Success", description }: ToastOptions) {
  toast.add({ title, description, type: "success" });
}

export interface MutationToastConfig<TData = void> {
  successMessage: string | ((data: TData) => string);
  errorMessage?: string | ((error: unknown) => string);
  successTitle?: string;
  errorTitle?: string;
  showSuccess?: boolean;
  showError?: boolean;
}

export function mergeMutationHandlers<TData>(
  toastConfig: MutationToastConfig<TData>,
  handlers?: {
    onSuccess?: (data: TData) => void;
    onError?: (error: unknown) => void;
  },
) {
  const showSuccess = toastConfig.showSuccess ?? true;
  const showError = toastConfig.showError ?? true;

  return {
    onSuccess: (data: TData) => {
      handlers?.onSuccess?.(data);
      if (showSuccess) {
        const description =
          typeof toastConfig.successMessage === "function"
            ? toastConfig.successMessage(data)
            : toastConfig.successMessage;
        showSuccessToast({
          title: toastConfig.successTitle ?? "Success",
          description,
        });
      }
    },
    onError: (error: unknown) => {
      handlers?.onError?.(error);
      if (showError) {
        const description =
          typeof toastConfig.errorMessage === "function"
            ? toastConfig.errorMessage(error)
            : toastConfig.errorMessage ?? getErrorMessage(error);
        showErrorToast({
          title: toastConfig.errorTitle ?? "Error",
          description,
        });
      }
    },
  };
}
