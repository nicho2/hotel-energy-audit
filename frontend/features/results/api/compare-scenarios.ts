import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ScenarioComparisonResponse } from "@/types/results";

export async function compareScenarios(
  projectId: string,
  scenarioIds: string[],
  token?: string | null,
): Promise<ApiEnvelope<ScenarioComparisonResponse>> {
  return apiClient.post<ScenarioComparisonResponse>(
    `/api/v1/projects/${projectId}/scenarios/compare`,
    { scenario_ids: scenarioIds },
    token,
  );
}
