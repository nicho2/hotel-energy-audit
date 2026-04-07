import type { ApiEnvelope, ApiErrorShape } from "@/types/api";

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

export function toApiError(status: number, payload: ApiEnvelope<unknown> | null): ApiError {
  return new ApiError(
    payload?.errors?.[0]?.message ?? "API request failed",
    status,
    payload?.errors ?? [],
  );
}
