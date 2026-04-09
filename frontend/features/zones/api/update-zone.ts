import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { BuildingZoneResponse, BuildingZoneUpdatePayload } from "@/types/zones";

export async function updateZone(
  projectId: string,
  zoneId: string,
  payload: BuildingZoneUpdatePayload,
  token?: string | null,
): Promise<ApiEnvelope<BuildingZoneResponse>> {
  return apiClient.patch<BuildingZoneResponse>(`/api/v1/projects/${projectId}/zones/${zoneId}`, payload, token);
}
