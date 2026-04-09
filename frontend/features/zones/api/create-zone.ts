import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { BuildingZoneCreatePayload, BuildingZoneResponse } from "@/types/zones";

export async function createZone(
  projectId: string,
  payload: BuildingZoneCreatePayload,
  token?: string | null,
): Promise<ApiEnvelope<BuildingZoneResponse>> {
  return apiClient.post<BuildingZoneResponse>(`/api/v1/projects/${projectId}/zones`, payload, token);
}
