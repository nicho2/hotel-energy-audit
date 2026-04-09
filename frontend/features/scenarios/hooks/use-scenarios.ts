"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import type {
  ScenarioCreatePayload,
  ScenarioDuplicatePayload,
  ScenarioSolutionAssignmentCreatePayload,
  ScenarioSolutionAssignmentUpdatePayload,
  ScenarioUpdatePayload,
} from "@/types/scenarios";
import { createScenario } from "../api/create-scenario";
import { createScenarioSolution } from "../api/create-scenario-solution";
import { deleteScenarioSolution } from "../api/delete-scenario-solution";
import { duplicateScenario } from "../api/duplicate-scenario";
import { listScenarioSolutions } from "../api/list-scenario-solutions";
import { listScenarios } from "../api/list-scenarios";
import { listSolutionCatalog } from "../api/list-solution-catalog";
import { updateScenario } from "../api/update-scenario";
import { updateScenarioSolution } from "../api/update-scenario-solution";

export function useScenarios(projectId: string, selectedScenarioId?: string | null) {
  const queryClient = useQueryClient();
  const { isReady, token } = useAuthContext();

  const scenarios = useQuery({
    queryKey: ["scenarios", projectId],
    queryFn: () => listScenarios(projectId, token),
    enabled: isReady && !!projectId,
  });

  const catalog = useQuery({
    queryKey: ["solutionCatalog"],
    queryFn: () => listSolutionCatalog(token),
    enabled: isReady,
  });

  const scenarioSolutions = useQuery({
    queryKey: ["scenarioSolutions", projectId, selectedScenarioId],
    queryFn: () => listScenarioSolutions(projectId, selectedScenarioId!, token),
    enabled: isReady && !!projectId && !!selectedScenarioId,
  });

  const invalidateScenarioData = async (scenarioId?: string | null) => {
    await queryClient.invalidateQueries({ queryKey: ["scenarios", projectId] });
    if (scenarioId) {
      await queryClient.invalidateQueries({ queryKey: ["scenarioSolutions", projectId, scenarioId] });
    }
  };

  const createScenarioMutation = useMutation({
    mutationFn: (payload: ScenarioCreatePayload) => createScenario(projectId, payload, token),
    onSuccess: async () => invalidateScenarioData(),
  });

  const updateScenarioMutation = useMutation({
    mutationFn: ({ scenarioId, payload }: { scenarioId: string; payload: ScenarioUpdatePayload }) =>
      updateScenario(projectId, scenarioId, payload, token),
    onSuccess: async (_, variables) => invalidateScenarioData(variables.scenarioId),
  });

  const duplicateScenarioMutation = useMutation({
    mutationFn: ({ scenarioId, payload }: { scenarioId: string; payload: ScenarioDuplicatePayload }) =>
      duplicateScenario(projectId, scenarioId, payload, token),
    onSuccess: async () => invalidateScenarioData(),
  });

  const createAssignmentMutation = useMutation({
    mutationFn: ({ scenarioId, payload }: { scenarioId: string; payload: ScenarioSolutionAssignmentCreatePayload }) =>
      createScenarioSolution(projectId, scenarioId, payload, token),
    onSuccess: async (_, variables) => invalidateScenarioData(variables.scenarioId),
  });

  const updateAssignmentMutation = useMutation({
    mutationFn: ({ scenarioId, assignmentId, payload }: { scenarioId: string; assignmentId: string; payload: ScenarioSolutionAssignmentUpdatePayload }) =>
      updateScenarioSolution(projectId, scenarioId, assignmentId, payload, token),
    onSuccess: async (_, variables) => invalidateScenarioData(variables.scenarioId),
  });

  const deleteAssignmentMutation = useMutation({
    mutationFn: ({ scenarioId, assignmentId }: { scenarioId: string; assignmentId: string }) =>
      deleteScenarioSolution(projectId, scenarioId, assignmentId, token),
    onSuccess: async (_, variables) => invalidateScenarioData(variables.scenarioId),
  });

  return {
    scenarios,
    catalog,
    scenarioSolutions,
    createScenario: createScenarioMutation,
    updateScenario: updateScenarioMutation,
    duplicateScenario: duplicateScenarioMutation,
    createAssignment: createAssignmentMutation,
    updateAssignment: updateAssignmentMutation,
    deleteAssignment: deleteAssignmentMutation,
  };
}
