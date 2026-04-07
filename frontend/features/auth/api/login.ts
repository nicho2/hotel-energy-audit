import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { AuthUser } from "@/types/auth";

export type LoginPayload = {
  email: string;
  password: string;
};

export type LoginResponse = {
  access_token: string;
  user: AuthUser;
};

export async function login(payload: LoginPayload): Promise<ApiEnvelope<LoginResponse>> {
  return apiClient.post<LoginResponse>("/api/v1/auth/login", payload);
}
