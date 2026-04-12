"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import type { ProjectTemplateCreatePayload } from "@/types/templates";
import { createProjectTemplate } from "../api/create-project-template";
import { listProjectTemplates } from "../api/list-project-templates";

export function useProjectTemplates() {
  const queryClient = useQueryClient();
  const { isReady, token } = useAuthContext();

  const templates = useQuery({
    queryKey: ["projectTemplates"],
    queryFn: () => listProjectTemplates(token),
    enabled: isReady && !!token,
    retry: false,
  });

  const createTemplate = useMutation({
    mutationFn: (payload: ProjectTemplateCreatePayload) => createProjectTemplate(payload, token),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["projectTemplates"] });
    },
  });

  return { templates, createTemplate };
}
