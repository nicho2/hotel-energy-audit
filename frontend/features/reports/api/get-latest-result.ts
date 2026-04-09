import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { CalculationResultLatestResponse } from "@/types/reports";

export async function getLatestResult(
  projectId: string,
  scenarioId: string,
  token?: string | null,
): Promise<ApiEnvelope<CalculationResultLatestResponse>> {
  return apiClient.get<CalculationResultLatestResponse>(
    `/api/v1/projects/${projectId}/scenarios/${scenarioId}/results/latest`,
    token,
  );
}
