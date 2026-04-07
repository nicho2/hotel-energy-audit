"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client/client";
import { useAuthContext } from "@/providers/auth-provider";
import type { ApiEnvelope } from "@/types/api";
import type { BuildingPayload, BuildingResponse } from "@/types/building";
import { upsertBuilding } from "../api/upsert-building";

async function getBuilding(projectId: string, token?: string | null): Promise<ApiEnvelope<BuildingResponse | null>> {
  return apiClient.get<BuildingResponse | null>(`/api/v1/projects/${projectId}/building`, token);
}

export function useBuilding(projectId: string) {
  const queryClient = useQueryClient();
  const { isReady, token } = useAuthContext();

  const buildingQuery = useQuery({
    queryKey: ["building", projectId],
    queryFn: () => getBuilding(projectId, token),
    enabled: isReady && !!projectId,
  });

  const saveBuilding = useMutation({
    mutationFn: (payload: BuildingPayload) => upsertBuilding(projectId, payload, token),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["building", projectId] });
      await queryClient.invalidateQueries({ queryKey: ["wizard", projectId] });
    },
  });

  return {
    ...buildingQuery,
    saveBuilding,
  };
}
