"use client";

import { useQuery } from "@tanstack/react-query";
import { listProjects } from "../api/list-projects";
import { useAuthContext } from "@/providers/auth-provider";

export function useProjects() {
  const { token } = useAuthContext();

  return useQuery({
    queryKey: ["projects"],
    queryFn: () => listProjects(token),
  });
}
