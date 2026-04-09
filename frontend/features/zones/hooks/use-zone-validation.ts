"use client";

import { useQuery } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import { getZoneValidation } from "../api/get-zone-validation";

export function useZoneValidation(projectId: string) {
  const { isReady, token } = useAuthContext();

  return useQuery({
    queryKey: ["zoneValidation", projectId],
    queryFn: () => getZoneValidation(projectId, token),
    enabled: isReady && !!projectId,
  });
}
