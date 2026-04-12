import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { WizardStepSaveResponse } from "@/types/wizard";

export async function saveStep(
  projectId: string,
  stepCode: string,
  payload: unknown,
  token?: string | null,
): Promise<ApiEnvelope<WizardStepSaveResponse>> {
  return apiClient.put<WizardStepSaveResponse>(
    `/api/v1/projects/${projectId}/wizard/steps/${stepCode}`,
    { payload },
    token,
  );
}
