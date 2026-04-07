import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ProjectCreatePayload, ProjectResponse } from "@/types/project";

export async function createProject(
  payload: ProjectCreatePayload,
  token?: string | null,
): Promise<ApiEnvelope<ProjectResponse>> {
  return apiClient.post<ProjectResponse>("/api/v1/projects", payload, token);
}
