"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import type { BacsAssessmentUpsertPayload, BacsCurrentFunctionsUpdatePayload } from "@/types/bacs";
import { getBacsSummary } from "../api/get-bacs-summary";
import { getCurrentBacs } from "../api/get-current-bacs";
import { replaceCurrentFunctions } from "../api/replace-current-functions";
import { upsertCurrentBacs } from "../api/upsert-current-bacs";

export function useBacs(projectId: string) {
  const queryClient = useQueryClient();
  const { isReady, token } = useAuthContext();

  const currentQuery = useQuery({
    queryKey: ["bacsCurrent", projectId],
    queryFn: () => getCurrentBacs(projectId, token),
    enabled: isReady && !!projectId,
  });

  const summaryQuery = useQuery({
    queryKey: ["bacsSummary", projectId],
    queryFn: () => getBacsSummary(projectId, token),
    enabled: isReady && !!projectId,
  });

  const invalidateRelatedQueries = async () => {
    await queryClient.invalidateQueries({ queryKey: ["bacsCurrent", projectId] });
    await queryClient.invalidateQueries({ queryKey: ["bacsSummary", projectId] });
    await queryClient.invalidateQueries({ queryKey: ["wizard", projectId] });
  };

  const saveAssessment = useMutation({
    mutationFn: (payload: BacsAssessmentUpsertPayload) => upsertCurrentBacs(projectId, payload, token),
    onSuccess: invalidateRelatedQueries,
  });

  const saveFunctions = useMutation({
    mutationFn: (payload: BacsCurrentFunctionsUpdatePayload) => replaceCurrentFunctions(projectId, payload, token),
    onSuccess: invalidateRelatedQueries,
  });

  return {
    current: currentQuery,
    summary: summaryQuery,
    saveAssessment,
    saveFunctions,
  };
}
