import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ScenarioCreatePayload, ScenarioResponse } from "@/types/scenarios";

export async function createScenario(projectId: string, payload: ScenarioCreatePayload, token?: string | null): Promise<ApiEnvelope<ScenarioResponse>> {
  return apiClient.post<ScenarioResponse>(`/api/v1/projects/${projectId}/scenarios`, payload, token);
}
