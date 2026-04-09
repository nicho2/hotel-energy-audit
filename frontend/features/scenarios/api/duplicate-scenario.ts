import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ScenarioDuplicatePayload, ScenarioResponse } from "@/types/scenarios";

export async function duplicateScenario(projectId: string, scenarioId: string, payload: ScenarioDuplicatePayload, token?: string | null): Promise<ApiEnvelope<ScenarioResponse>> {
  return apiClient.post<ScenarioResponse>(`/api/v1/projects/${projectId}/scenarios/${scenarioId}/duplicate`, payload, token);
}
