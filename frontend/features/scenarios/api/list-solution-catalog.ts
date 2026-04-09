import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { SolutionCatalogItem } from "@/types/scenarios";

export async function listSolutionCatalog(token?: string | null): Promise<ApiEnvelope<SolutionCatalogItem[]>> {
  return apiClient.get<SolutionCatalogItem[]>(`/api/v1/projects/solutions/catalog`, token);
}
