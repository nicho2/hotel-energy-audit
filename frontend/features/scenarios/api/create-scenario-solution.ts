import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ScenarioSolutionAssignment, ScenarioSolutionAssignmentCreatePayload } from "@/types/scenarios";

export async function createScenarioSolution(projectId: string, scenarioId: string, payload: ScenarioSolutionAssignmentCreatePayload, token?: string | null): Promise<ApiEnvelope<ScenarioSolutionAssignment>> {
  return apiClient.post<ScenarioSolutionAssignment>(`/api/v1/projects/${projectId}/scenarios/${scenarioId}/solutions`, payload, token);
}
