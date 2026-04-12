import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { CountryProfile } from "@/types/reference-data";

export async function listCountryProfiles(token?: string | null): Promise<ApiEnvelope<CountryProfile[]>> {
  return apiClient.get<CountryProfile[]>("/api/v1/country-profiles", token);
}
