"use client";

import { useQuery } from "@tanstack/react-query";
import { getWizard } from "../api/get-wizard";
import { useAuthContext } from "@/providers/auth-provider";

export function useWizard(projectId: string) {
  const { isReady, token } = useAuthContext();

  return useQuery({
    queryKey: ["wizard", projectId],
    queryFn: () => getWizard(projectId, token),
    enabled: isReady && !!projectId,
  });
}
