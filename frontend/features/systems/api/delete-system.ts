import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { TechnicalSystemResponse } from "@/types/systems";

export async function deleteSystem(
  projectId: string,
  systemId: string,
  token?: string | null,
): Promise<ApiEnvelope<TechnicalSystemResponse>> {
  return apiClient.delete<TechnicalSystemResponse>(`/api/v1/projects/${projectId}/systems/${systemId}`, token);
}
