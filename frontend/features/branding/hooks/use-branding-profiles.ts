"use client";

import { useQuery } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import { listBrandingProfiles } from "../api/list-branding-profiles";

export function useBrandingProfiles() {
  const { isReady, token } = useAuthContext();

  return useQuery({
    queryKey: ["branding", "profiles"],
    queryFn: () => listBrandingProfiles(token),
    enabled: isReady && !!token,
    retry: false,
  });
}
