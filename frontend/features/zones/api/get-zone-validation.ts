import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ZoneValidationResponse } from "@/types/zones";

export async function getZoneValidation(
  projectId: string,
  token?: string | null,
): Promise<ApiEnvelope<ZoneValidationResponse>> {
  return apiClient.get<ZoneValidationResponse>(`/api/v1/projects/${projectId}/zones/validation`, token);
}
