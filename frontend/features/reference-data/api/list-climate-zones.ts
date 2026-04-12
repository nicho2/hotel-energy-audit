import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ClimateZone } from "@/types/reference-data";

export async function listClimateZones(
  countryProfileId?: string | null,
  token?: string | null,
): Promise<ApiEnvelope<ClimateZone[]>> {
  const query = countryProfileId ? `?country_profile_id=${encodeURIComponent(countryProfileId)}` : "";
  return apiClient.get<ClimateZone[]>(`/api/v1/climate-zones${query}`, token);
}
