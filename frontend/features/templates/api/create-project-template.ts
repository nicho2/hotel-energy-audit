import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ProjectTemplate, ProjectTemplateCreatePayload } from "@/types/templates";

export async function createProjectTemplate(
  payload: ProjectTemplateCreatePayload,
  token?: string | null,
): Promise<ApiEnvelope<ProjectTemplate>> {
  return apiClient.post<ProjectTemplate>("/api/v1/project-templates", payload, token);
}
