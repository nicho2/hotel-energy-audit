import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ProjectAssumptions } from "@/types/assumptions";

export async function getProjectAssumptions(
  projectId: string,
  token?: string | null,
): Promise<ApiEnvelope<ProjectAssumptions>> {
  return apiClient.get<ProjectAssumptions>(`/api/v1/projects/${projectId}/assumptions`, token);
}
