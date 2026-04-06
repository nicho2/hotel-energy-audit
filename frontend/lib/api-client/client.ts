import { env } from "@/lib/config/env";

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

async function request<T>(path: string, method: HttpMethod, body?: unknown, token?: string | null): Promise<T> {
  const response = await fetch(`${env.apiBaseUrl}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  const json = await response.json();

  if (!response.ok) {
    throw new Error(json?.errors?.[0]?.message ?? "API request failed");
  }

  return json;
}

export const apiClient = {
  get: <T>(path: string, token?: string | null) => request<T>(path, "GET", undefined, token),
  post: <T>(path: string, body?: unknown, token?: string | null) => request<T>(path, "POST", body, token),
  put: <T>(path: string, body?: unknown, token?: string | null) => request<T>(path, "PUT", body, token),
  patch: <T>(path: string, body?: unknown, token?: string | null) => request<T>(path, "PATCH", body, token),
  delete: <T>(path: string, token?: string | null) => request<T>(path, "DELETE", undefined, token),
};
