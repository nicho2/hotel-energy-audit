import { apiClient } from "@/lib/api-client/client";

export async function getWizard(projectId: string, token?: string | null) {
  return apiClient.get(`/api/v1/projects/${projectId}/wizard`, token);
}
