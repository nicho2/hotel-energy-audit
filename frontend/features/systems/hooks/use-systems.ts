"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import type { TechnicalSystemCreatePayload, TechnicalSystemUpdatePayload } from "@/types/systems";
import { createSystem } from "../api/create-system";
import { deleteSystem } from "../api/delete-system";
import { listSystems } from "../api/list-systems";
import { updateSystem } from "../api/update-system";

export function useSystems(projectId: string) {
  const queryClient = useQueryClient();
  const { isReady, token } = useAuthContext();

  const systemsQuery = useQuery({
    queryKey: ["systems", projectId],
    queryFn: () => listSystems(projectId, token),
    enabled: isReady && !!projectId,
  });

  const invalidateRelatedQueries = async () => {
    await queryClient.invalidateQueries({ queryKey: ["systems", projectId] });
    await queryClient.invalidateQueries({ queryKey: ["wizard", projectId] });
  };

  const createSystemMutation = useMutation({
    mutationFn: (payload: TechnicalSystemCreatePayload) => createSystem(projectId, payload, token),
    onSuccess: invalidateRelatedQueries,
  });

  const updateSystemMutation = useMutation({
    mutationFn: ({ systemId, payload }: { systemId: string; payload: TechnicalSystemUpdatePayload }) =>
      updateSystem(projectId, systemId, payload, token),
    onSuccess: invalidateRelatedQueries,
  });

  const deleteSystemMutation = useMutation({
    mutationFn: (systemId: string) => deleteSystem(projectId, systemId, token),
    onSuccess: invalidateRelatedQueries,
  });

  return {
    ...systemsQuery,
    createSystem: createSystemMutation,
    updateSystem: updateSystemMutation,
    deleteSystem: deleteSystemMutation,
  };
}
