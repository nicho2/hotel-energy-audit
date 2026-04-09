"use client";

import { useMutation } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import { compareScenarios } from "../api/compare-scenarios";

export function useScenarioComparison(projectId: string) {
  const { token } = useAuthContext();

  return useMutation({
    mutationFn: (scenarioIds: string[]) => compareScenarios(projectId, scenarioIds, token),
  });
}
