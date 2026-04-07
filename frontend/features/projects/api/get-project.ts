import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ProjectResponse } from "@/types/project";

export async function getProject(projectId: string, token?: string | null): Promise<ApiEnvelope<ProjectResponse>> {
  return apiClient.get<ProjectResponse>(`/api/v1/projects/${projectId}`, token);
}
