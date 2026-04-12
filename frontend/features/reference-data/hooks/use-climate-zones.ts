"use client";

import { useQuery } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import { listClimateZones } from "../api/list-climate-zones";

export function useClimateZones(countryProfileId?: string | null) {
  const { isReady, token } = useAuthContext();

  return useQuery({
    queryKey: ["reference-data", "climate-zones", countryProfileId ?? ""],
    queryFn: () => listClimateZones(countryProfileId, token),
    enabled: isReady && !!token && !!countryProfileId,
    retry: false,
  });
}
