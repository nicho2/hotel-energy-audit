import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { BuildingPayload, BuildingResponse } from "@/types/building";

export async function upsertBuilding(
  projectId: string,
  payload: BuildingPayload,
  token?: string | null,
): Promise<ApiEnvelope<BuildingResponse>> {
  return apiClient.put<BuildingResponse>(`/api/v1/projects/${projectId}/building`, payload, token);
}
