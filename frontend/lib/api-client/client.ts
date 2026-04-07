import { env } from "@/lib/config/env";
import { ApiError, toApiError } from "@/lib/api-client/errors";
import type { ApiEnvelope, ApiRequestOptions } from "@/types/api";

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

async function request<T>(
  path: string,
  method: HttpMethod,
  options: ApiRequestOptions = {},
): Promise<ApiEnvelope<T>> {
  const { body, headers, token } = options;
  const response = await fetch(`${env.apiBaseUrl}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
    cache: "no-store",
  });

  const rawText = await response.text();
  const json = rawText ? (JSON.parse(rawText) as ApiEnvelope<T>) : null;

  if (!response.ok) {
    throw toApiError(response.status, json);
  }

  return (
    json ?? {
      data: null as T,
      meta: {},
      errors: [],
    }
  );
}

export const apiClient = {
  get: <T>(path: string, token?: string | null) => request<T>(path, "GET", { token }),
  post: <T>(path: string, body?: unknown, token?: string | null) => request<T>(path, "POST", { body, token }),
  put: <T>(path: string, body?: unknown, token?: string | null) => request<T>(path, "PUT", { body, token }),
  patch: <T>(path: string, body?: unknown, token?: string | null) => request<T>(path, "PATCH", { body, token }),
  delete: <T>(path: string, token?: string | null) => request<T>(path, "DELETE", { token }),
};

export { ApiError };
