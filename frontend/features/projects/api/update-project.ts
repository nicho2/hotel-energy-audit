import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ProjectResponse, ProjectUpdatePayload } from "@/types/project";

export async function updateProject(
  projectId: string,
  payload: ProjectUpdatePayload,
  token?: string | null,
): Promise<ApiEnvelope<ProjectResponse>> {
  return apiClient.patch<ProjectResponse>(`/api/v1/projects/${projectId}`, payload, token);
}
