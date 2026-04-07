import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ProjectListItem } from "@/types/project";

export async function listProjects(token?: string | null): Promise<ApiEnvelope<ProjectListItem[]>> {
  return apiClient.get<ProjectListItem[]>("/api/v1/projects", token);
}
