import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { BacsSummaryResponse } from "@/types/bacs";

export async function getBacsSummary(
  projectId: string,
  token?: string | null,
): Promise<ApiEnvelope<BacsSummaryResponse>> {
  return apiClient.get<BacsSummaryResponse>(`/api/v1/projects/${projectId}/bacs/current/summary`, token);
}
