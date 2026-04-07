export type ApiErrorShape = {
  code: string;
  message: string;
  field?: string;
  details?: Record<string, unknown>;
};

export type ApiEnvelope<T> = {
  data: T;
  meta: Record<string, unknown>;
  errors: ApiErrorShape[];
};

export type ApiRequestOptions = {
  token?: string | null;
  body?: unknown;
  headers?: HeadersInit;
};
