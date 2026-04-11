"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/auth-provider";
import type { AdminUserCreatePayload } from "@/types/admin";
import { createAdminUser, deactivateAdminUser, listAdminUsers } from "../api/admin-api";

export function useAdminUsers() {
  const queryClient = useQueryClient();
  const { isReady, token, user } = useAuthContext();
  const enabled = isReady && !!token && user?.role === "org_admin";

  const users = useQuery({
    queryKey: ["admin", "users"],
    queryFn: () => listAdminUsers(token),
    enabled,
  });

  const createUser = useMutation({
    mutationFn: (payload: AdminUserCreatePayload) => createAdminUser(payload, token),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["admin", "users"] });
    },
  });

  const deactivateUser = useMutation({
    mutationFn: (userId: string) => deactivateAdminUser(userId, token),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["admin", "users"] });
    },
  });

  return { users, createUser, deactivateUser };
}
