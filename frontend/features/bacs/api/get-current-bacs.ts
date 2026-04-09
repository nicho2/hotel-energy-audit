import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { BacsCurrentResponse } from "@/types/bacs";

export async function getCurrentBacs(
  projectId: string,
  token?: string | null,
): Promise<ApiEnvelope<BacsCurrentResponse>> {
  return apiClient.get<BacsCurrentResponse>(`/api/v1/projects/${projectId}/bacs/current`, token);
}
