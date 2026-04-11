import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type {
  AdminBrandingCreatePayload,
  AdminBrandingUpdatePayload,
  AdminUser,
  AdminUserCreatePayload,
} from "@/types/admin";
import type { BrandingProfile } from "@/types/branding";

export function listAdminUsers(token?: string | null): Promise<ApiEnvelope<AdminUser[]>> {
  return apiClient.get<AdminUser[]>("/api/v1/admin/users", token);
}

export function createAdminUser(
  payload: AdminUserCreatePayload,
  token?: string | null,
): Promise<ApiEnvelope<AdminUser>> {
  return apiClient.post<AdminUser>("/api/v1/admin/users", payload, token);
}

export function deactivateAdminUser(userId: string, token?: string | null): Promise<ApiEnvelope<AdminUser>> {
  return apiClient.post<AdminUser>(`/api/v1/admin/users/${userId}/deactivate`, undefined, token);
}

export function listAdminBranding(token?: string | null): Promise<ApiEnvelope<BrandingProfile[]>> {
  return apiClient.get<BrandingProfile[]>("/api/v1/admin/branding", token);
}

export function createAdminBranding(
  payload: AdminBrandingCreatePayload,
  token?: string | null,
): Promise<ApiEnvelope<BrandingProfile>> {
  return apiClient.post<BrandingProfile>("/api/v1/admin/branding", payload, token);
}

export function updateAdminBranding(
  profileId: string,
  payload: AdminBrandingUpdatePayload,
  token?: string | null,
): Promise<ApiEnvelope<BrandingProfile>> {
  return apiClient.patch<BrandingProfile>(`/api/v1/admin/branding/${profileId}`, payload, token);
}
