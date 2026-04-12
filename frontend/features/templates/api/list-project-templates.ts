import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ProjectTemplate } from "@/types/templates";

export async function listProjectTemplates(token?: string | null): Promise<ApiEnvelope<ProjectTemplate[]>> {
  return apiClient.get<ProjectTemplate[]>("/api/v1/project-templates", token);
}
