import { apiClient, ApiError } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ZoneValidationResponse } from "@/types/zones";

export type StepValidationResult = {
  step_code: string;
  valid: boolean;
  message: string;
};

export async function validateStep(
  projectId: string,
  stepCode: string,
  token?: string | null,
): Promise<ApiEnvelope<StepValidationResult>> {
  if (stepCode === "zones") {
    const validation = await apiClient.get<ZoneValidationResponse>(`/api/v1/projects/${projectId}/zones/validation`, token);

    if (!validation.data.is_valid) {
      const errorMessage =
        validation.data.checks.find((item) => item.status === "error")?.message ??
        "La validation des zones a echoue.";

      throw new ApiError(errorMessage, 422, [
        {
          code: "ZONE_VALIDATION_ERROR",
          message: errorMessage,
        },
      ]);
    }

    return {
      data: {
        step_code: stepCode,
        valid: true,
        message: "Zones validation passed.",
      },
      meta: {},
      errors: [],
    };
  }

  // Placeholder facade: keeps a stable call site until backend step validation endpoints exist.
  return Promise.resolve({
    data: {
      step_code: stepCode,
      valid: true,
      message: `Validation placeholder for ${projectId}/${stepCode}.`,
    },
    meta: {},
    errors: [],
  });
}
