import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { BuildingZoneGeneratePayload, BuildingZoneResponse } from "@/types/zones";

export async function generateZones(
  projectId: string,
  payload: BuildingZoneGeneratePayload,
  token?: string | null,
): Promise<ApiEnvelope<BuildingZoneResponse[]>> {
  return apiClient.post<BuildingZoneResponse[]>(`/api/v1/projects/${projectId}/zones/generate`, payload, token);
}
