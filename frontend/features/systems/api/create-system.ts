import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { TechnicalSystemCreatePayload, TechnicalSystemResponse } from "@/types/systems";

export async function createSystem(
  projectId: string,
  payload: TechnicalSystemCreatePayload,
  token?: string | null,
): Promise<ApiEnvelope<TechnicalSystemResponse>> {
  return apiClient.post<TechnicalSystemResponse>(`/api/v1/projects/${projectId}/systems`, payload, token);
}
