"use client";

import { useQuery } from "@tanstack/react-query";
import { getProject } from "../api/get-project";
import { useAuthContext } from "@/providers/auth-provider";

export function useProject(projectId: string) {
  const { isReady, token } = useAuthContext();

  return useQuery({
    queryKey: ["project", projectId],
    queryFn: () => getProject(projectId, token),
    enabled: isReady && !!projectId,
  });
}
