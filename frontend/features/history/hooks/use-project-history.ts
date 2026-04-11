"use client";

import { useQuery } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import { listProjectHistory } from "../api/list-project-history";

export function useProjectHistory(projectId: string) {
  const { isReady, token } = useAuthContext();

  return useQuery({
    queryKey: ["project", projectId, "history"],
    queryFn: () => listProjectHistory(projectId, token),
    enabled: isReady && !!projectId,
  });
}
