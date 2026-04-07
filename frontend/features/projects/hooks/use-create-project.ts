"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createProject } from "../api/create-project";
import { useAuthContext } from "@/providers/auth-provider";
import type { ProjectCreatePayload } from "@/types/project";

export function useCreateProject() {
  const queryClient = useQueryClient();
  const { token } = useAuthContext();

  return useMutation({
    mutationFn: (payload: ProjectCreatePayload) => createProject(payload, token),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["projects"] });
    },
  });
}
