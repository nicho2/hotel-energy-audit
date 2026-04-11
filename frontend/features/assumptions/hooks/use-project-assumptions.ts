"use client";

import { useQuery } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import { getProjectAssumptions } from "../api/get-project-assumptions";

export function useProjectAssumptions(projectId: string) {
  const { isReady, token } = useAuthContext();

  return useQuery({
    queryKey: ["project", projectId, "assumptions"],
    queryFn: () => getProjectAssumptions(projectId, token),
    enabled: isReady && !!projectId,
  });
}
