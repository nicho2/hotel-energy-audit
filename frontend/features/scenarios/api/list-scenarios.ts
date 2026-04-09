import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ScenarioResponse } from "@/types/scenarios";

export async function listScenarios(projectId: string, token?: string | null): Promise<ApiEnvelope<ScenarioResponse[]>> {
  return apiClient.get<ScenarioResponse[]>(`/api/v1/projects/${projectId}/scenarios`, token);
}
