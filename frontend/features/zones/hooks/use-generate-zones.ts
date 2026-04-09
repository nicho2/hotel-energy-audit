"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import type { BuildingZoneGeneratePayload } from "@/types/zones";
import { generateZones } from "../api/generate-zones";

export function useGenerateZones(projectId: string) {
  const queryClient = useQueryClient();
  const { token } = useAuthContext();

  return useMutation({
    mutationFn: (payload: BuildingZoneGeneratePayload) => generateZones(projectId, payload, token),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["zones", projectId] });
      await queryClient.invalidateQueries({ queryKey: ["zoneValidation", projectId] });
      await queryClient.invalidateQueries({ queryKey: ["wizard", projectId] });
    },
  });
}
