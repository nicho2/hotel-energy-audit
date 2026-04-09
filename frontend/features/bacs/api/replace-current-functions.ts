import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { BacsCurrentFunctionsUpdatePayload, BacsCurrentResponse } from "@/types/bacs";

export async function replaceCurrentFunctions(
  projectId: string,
  payload: BacsCurrentFunctionsUpdatePayload,
  token?: string | null,
): Promise<ApiEnvelope<BacsCurrentResponse>> {
  return apiClient.put<BacsCurrentResponse>(`/api/v1/projects/${projectId}/bacs/current/functions`, payload, token);
}
