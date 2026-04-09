import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ScenarioResponse, ScenarioUpdatePayload } from "@/types/scenarios";

export async function updateScenario(projectId: string, scenarioId: string, payload: ScenarioUpdatePayload, token?: string | null): Promise<ApiEnvelope<ScenarioResponse>> {
  return apiClient.patch<ScenarioResponse>(`/api/v1/projects/${projectId}/scenarios/${scenarioId}`, payload, token);
}
