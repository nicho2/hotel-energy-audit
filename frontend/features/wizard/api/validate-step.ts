import type { ApiEnvelope } from "@/types/api";

export type StepValidationResult = {
  step_code: string;
  valid: boolean;
  message: string;
};

export async function validateStep(projectId: string, stepCode: string): Promise<ApiEnvelope<StepValidationResult>> {
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
