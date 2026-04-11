"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import type { AdminBrandingCreatePayload, AdminBrandingUpdatePayload } from "@/types/admin";
import { createAdminBranding, listAdminBranding, updateAdminBranding } from "../api/admin-api";

export function useAdminBranding() {
  const queryClient = useQueryClient();
  const { isReady, token, user } = useAuthContext();
  const enabled = isReady && !!token && user?.role === "org_admin";

  const branding = useQuery({
    queryKey: ["admin", "branding"],
    queryFn: () => listAdminBranding(token),
    enabled,
  });

  const createBranding = useMutation({
    mutationFn: (payload: AdminBrandingCreatePayload) => createAdminBranding(payload, token),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["admin", "branding"] });
      await queryClient.invalidateQueries({ queryKey: ["branding", "profiles"] });
    },
  });

  const updateBranding = useMutation({
    mutationFn: ({ profileId, payload }: { profileId: string; payload: AdminBrandingUpdatePayload }) =>
      updateAdminBranding(profileId, payload, token),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["admin", "branding"] });
      await queryClient.invalidateQueries({ queryKey: ["branding", "profiles"] });
    },
  });

  return { branding, createBranding, updateBranding };
}
