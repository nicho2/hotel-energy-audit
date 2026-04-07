import { env } from "@/lib/config/env";
import type { ApiEnvelope, ApiErrorShape } from "@/types/api";

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export class ApiError extends Error {
  readonly status: number;
  readonly errors: ApiErrorShape[];

  constructor(message: string, status: number, errors: ApiErrorShape[] = []) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.errors = errors;
  }
}

async function request<T>(
  path: string,
  method: HttpMethod,
  body?: unknown,
  token?: string | null,
): Promise<ApiEnvelope<T>> {
  const response = await fetch(`${env.apiBaseUrl}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
    cache: "no-store",
  });

  const rawText = await response.text();
  const json = rawText ? (JSON.parse(rawText) as ApiEnvelope<T>) : null;

  if (!response.ok) {
    throw new ApiError(
      json?.errors?.[0]?.message ?? "API request failed",
      response.status,
      json?.errors ?? [],
    );
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
  get: <T>(path: string, token?: string | null) => request<T>(path, "GET", undefined, token),
  post: <T>(path: string, body?: unknown, token?: string | null) => request<T>(path, "POST", body, token),
  put: <T>(path: string, body?: unknown, token?: string | null) => request<T>(path, "PUT", body, token),
  patch: <T>(path: string, body?: unknown, token?: string | null) => request<T>(path, "PATCH", body, token),
  delete: <T>(path: string, token?: string | null) => request<T>(path, "DELETE", undefined, token),
};
