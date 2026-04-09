"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import type { BuildingZoneCreatePayload, BuildingZoneUpdatePayload } from "@/types/zones";
import { createZone } from "../api/create-zone";
import { deleteZone } from "../api/delete-zone";
import { listZones } from "../api/list-zones";
import { updateZone } from "../api/update-zone";

export function useZones(projectId: string) {
  const queryClient = useQueryClient();
  const { isReady, token } = useAuthContext();

  const zonesQuery = useQuery({
    queryKey: ["zones", projectId],
    queryFn: () => listZones(projectId, token),
    enabled: isReady && !!projectId,
  });

  const invalidateRelatedQueries = async () => {
    await queryClient.invalidateQueries({ queryKey: ["zones", projectId] });
    await queryClient.invalidateQueries({ queryKey: ["zoneValidation", projectId] });
    await queryClient.invalidateQueries({ queryKey: ["wizard", projectId] });
  };

  const createZoneMutation = useMutation({
    mutationFn: (payload: BuildingZoneCreatePayload) => createZone(projectId, payload, token),
    onSuccess: invalidateRelatedQueries,
  });

  const updateZoneMutation = useMutation({
    mutationFn: ({ zoneId, payload }: { zoneId: string; payload: BuildingZoneUpdatePayload }) =>
      updateZone(projectId, zoneId, payload, token),
    onSuccess: invalidateRelatedQueries,
  });

  const deleteZoneMutation = useMutation({
    mutationFn: (zoneId: string) => deleteZone(projectId, zoneId, token),
    onSuccess: invalidateRelatedQueries,
  });

  return {
    ...zonesQuery,
    createZone: createZoneMutation,
    updateZone: updateZoneMutation,
    deleteZone: deleteZoneMutation,
  };
}
