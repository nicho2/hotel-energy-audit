import { apiClient } from "@/lib/api-client/client";

export async function login(payload: { email: string; password: string }) {
  return apiClient.post("/api/v1/auth/login", payload);
}
