"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import { listScenarios } from "@/features/scenarios/api/list-scenarios";
import { generateExecutiveReport } from "../api/generate-executive-report";
import { getLatestResult } from "../api/get-latest-result";
import { listProjectReports } from "../api/list-project-reports";

export function useReports(projectId: string, selectedScenarioId: string | null) {
  const queryClient = useQueryClient();
  const { isReady, token } = useAuthContext();

  const scenarios = useQuery({
    queryKey: ["reports", "scenarios", projectId],
    queryFn: () => listScenarios(projectId, token),
    enabled: isReady && !!projectId,
  });

  const reports = useQuery({
    queryKey: ["reports", "history", projectId],
    queryFn: () => listProjectReports(projectId, token),
    enabled: isReady && !!projectId,
  });

  const latestResult = useQuery({
    queryKey: ["reports", "latestResult", projectId, selectedScenarioId],
    queryFn: () => getLatestResult(projectId, selectedScenarioId!, token),
    enabled: isReady && !!projectId && !!selectedScenarioId,
    retry: false,
  });

  const generateReport = useMutation({
    mutationFn: (calculationRunId: string) => generateExecutiveReport(calculationRunId, token),
    onSuccess: async (_, calculationRunId) => {
      await queryClient.invalidateQueries({ queryKey: ["reports", "history", projectId] });
      await queryClient.invalidateQueries({ queryKey: ["reports", "latestResult", projectId] });
      await queryClient.invalidateQueries({ queryKey: ["report", calculationRunId] });
    },
  });

  return {
    scenarios,
    reports,
    latestResult,
    generateReport,
    token,
  };
}
