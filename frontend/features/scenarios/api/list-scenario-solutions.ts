import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ScenarioSolutionAssignment } from "@/types/scenarios";

export async function listScenarioSolutions(projectId: string, scenarioId: string, token?: string | null): Promise<ApiEnvelope<ScenarioSolutionAssignment[]>> {
  return apiClient.get<ScenarioSolutionAssignment[]>(`/api/v1/projects/${projectId}/scenarios/${scenarioId}/solutions`, token);
}
