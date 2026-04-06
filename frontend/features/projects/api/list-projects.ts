import { apiClient } from "@/lib/api-client/client";

export async function listProjects(token?: string | null) {
  return apiClient.get("/api/v1/projects", token);
}
