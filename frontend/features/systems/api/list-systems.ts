import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { TechnicalSystemResponse } from "@/types/systems";

export async function listSystems(
  projectId: string,
  token?: string | null,
): Promise<ApiEnvelope<TechnicalSystemResponse[]>> {
  return apiClient.get<TechnicalSystemResponse[]>(`/api/v1/projects/${projectId}/systems`, token);
}
