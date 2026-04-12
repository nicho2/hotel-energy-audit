"use client";

import { useQuery } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import { listCountryProfiles } from "../api/list-country-profiles";

export function useCountryProfiles(enabled = true) {
  const { isReady, token } = useAuthContext();

  return useQuery({
    queryKey: ["reference-data", "country-profiles"],
    queryFn: () => listCountryProfiles(token),
    enabled: enabled && isReady && !!token,
    retry: false,
  });
}
