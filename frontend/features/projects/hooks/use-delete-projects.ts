"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import { deleteProject } from "../api/delete-project";

export function useDeleteProjects() {
  const queryClient = useQueryClient();
  const { token } = useAuthContext();

  return useMutation({
    mutationFn: async (projectIds: string[]) => {
      const results = [];
      for (const projectId of projectIds) {
        results.push(await deleteProject(projectId, token));
      }
      return results;
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["projects"] });
    },
  });
}
