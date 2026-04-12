import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { SolutionCatalogItem } from "@/types/scenarios";

export type SolutionCatalogFilters = {
  country?: string;
  family?: string;
  building_type?: string;
  zone_type?: string;
  scope?: string;
};

export async function listSolutionCatalog(
  token?: string | null,
  filters: SolutionCatalogFilters = {},
): Promise<ApiEnvelope<SolutionCatalogItem[]>> {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value) {
      params.set(key, value);
    }
  }
  const suffix = params.toString() ? `?${params.toString()}` : "";
  return apiClient.get<SolutionCatalogItem[]>(`/api/v1/projects/solutions/catalog${suffix}`, token);
}
