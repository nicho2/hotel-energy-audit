"use client";

import { useQuery } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import { listSolutionCatalog, type SolutionCatalogFilters } from "../api/list-solution-catalog";

export function useSolutionCatalog(filters: SolutionCatalogFilters) {
  const { isReady, token } = useAuthContext();

  return useQuery({
    queryKey: ["solutionCatalog", filters],
    queryFn: () => listSolutionCatalog(token, filters),
    enabled: isReady && !!token,
    retry: false,
  });
}
