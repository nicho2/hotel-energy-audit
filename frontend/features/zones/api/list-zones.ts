import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { BuildingZoneResponse } from "@/types/zones";

export async function listZones(
  projectId: string,
  token?: string | null,
): Promise<ApiEnvelope<BuildingZoneResponse[]>> {
  return apiClient.get<BuildingZoneResponse[]>(`/api/v1/projects/${projectId}/zones`, token);
}
