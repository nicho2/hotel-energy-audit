import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { BrandingProfile } from "@/types/branding";

export async function listBrandingProfiles(token?: string | null): Promise<ApiEnvelope<BrandingProfile[]>> {
  return apiClient.get<BrandingProfile[]>("/api/v1/branding", token);
}
