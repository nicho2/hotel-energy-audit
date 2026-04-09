import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ScenarioSolutionAssignment, ScenarioSolutionAssignmentUpdatePayload } from "@/types/scenarios";

export async function updateScenarioSolution(projectId: string, scenarioId: string, assignmentId: string, payload: ScenarioSolutionAssignmentUpdatePayload, token?: string | null): Promise<ApiEnvelope<ScenarioSolutionAssignment>> {
  return apiClient.patch<ScenarioSolutionAssignment>(`/api/v1/projects/${projectId}/scenarios/${scenarioId}/solutions/${assignmentId}`, payload, token);
}
