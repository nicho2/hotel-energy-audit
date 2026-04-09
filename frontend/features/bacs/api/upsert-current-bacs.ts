import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { BacsAssessmentUpsertPayload, BacsCurrentResponse } from "@/types/bacs";

export async function upsertCurrentBacs(
  projectId: string,
  payload: BacsAssessmentUpsertPayload,
  token?: string | null,
): Promise<ApiEnvelope<BacsCurrentResponse>> {
  return apiClient.post<BacsCurrentResponse>(`/api/v1/projects/${projectId}/bacs/current`, payload, token);
}
