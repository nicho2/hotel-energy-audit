import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { TechnicalSystemResponse, TechnicalSystemUpdatePayload } from "@/types/systems";

export async function updateSystem(
  projectId: string,
  systemId: string,
  payload: TechnicalSystemUpdatePayload,
  token?: string | null,
): Promise<ApiEnvelope<TechnicalSystemResponse>> {
  return apiClient.patch<TechnicalSystemResponse>(`/api/v1/projects/${projectId}/systems/${systemId}`, payload, token);
}
