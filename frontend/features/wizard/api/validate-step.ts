import { apiClient, ApiError } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { WizardStepValidationResult } from "@/types/wizard";

export async function validateStep(
  projectId: string,
  stepCode: string,
  token?: string | null,
): Promise<ApiEnvelope<WizardStepValidationResult>> {
  const validation = await apiClient.post<WizardStepValidationResult>(
    `/api/v1/projects/${projectId}/wizard/steps/${stepCode}/validate`,
    {},
    token,
  );

  if (!validation.data.valid) {
    const errorMessage =
      validation.data.validations.find((item) => item.status === "error")?.message ??
      "La validation de l'etape a echoue.";

    throw new ApiError(errorMessage, 422, [
      {
        code: "WIZARD_STEP_VALIDATION_ERROR",
        message: errorMessage,
      },
    ]);
  }

  return validation;
}
