const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

function formatApiDetail(detail: unknown): string {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (item && typeof item === "object" && "msg" in item) {
          const loc =
            "loc" in item && Array.isArray(item.loc)
              ? item.loc.filter((part) => part !== "body").join(" → ")
              : "";
          const msg = String((item as { msg: string }).msg);
          return loc ? `${loc}: ${msg}` : msg;
        }
        return String(item);
      })
      .join("; ");
  }
  return "Request failed";
}

let refreshPromise: Promise<boolean> | null = null;

async function tryRefreshSession(): Promise<boolean> {
  if (!refreshPromise) {
    refreshPromise = fetch(`${API_BASE_URL}/auth/refresh`, {
      method: "POST",
      credentials: "include",
    })
      .then((response) => response.ok)
      .catch(() => false)
      .finally(() => {
        refreshPromise = null;
      });
  }
  return refreshPromise;
}

function shouldAttemptRefresh(endpoint: string, status: number, retried: boolean) {
  if (retried || status !== 401) return false;
  return !endpoint.startsWith("/auth/login") && !endpoint.startsWith("/auth/signup");
}

export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {},
  retried = false,
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (shouldAttemptRefresh(endpoint, response.status, retried)) {
    const refreshed = await tryRefreshSession();
    if (refreshed) {
      return apiFetch<T>(endpoint, options, true);
    }
  }

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const detail = (body as { detail?: unknown }).detail;
    throw new ApiError(
      response.status,
      detail !== undefined ? formatApiDetail(detail) : response.statusText,
    );
  }

  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export { API_BASE_URL };
