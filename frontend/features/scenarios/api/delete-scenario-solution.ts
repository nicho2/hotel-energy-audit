import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ScenarioSolutionAssignment } from "@/types/scenarios";

export async function deleteScenarioSolution(projectId: string, scenarioId: string, assignmentId: string, token?: string | null): Promise<ApiEnvelope<ScenarioSolutionAssignment>> {
  return apiClient.delete<ScenarioSolutionAssignment>(`/api/v1/projects/${projectId}/scenarios/${scenarioId}/solutions/${assignmentId}`, token);
}
