export type WizardValidation = {
  code: string;
  status: "ok" | "warning" | "error" | "pending";
  message: string;
};

export type WizardStepStatus = "completed" | "current" | "not_started";

export type WizardStep = {
  step: number;
  code: string;
  name: string;
  status: WizardStepStatus;
  validations: WizardValidation[];
};

export type WizardReadiness = {
  status: "not_ready" | "ready";
  can_calculate: boolean;
  blocking_steps: number[];
  pending_validations: string[];
};

export type WizardState = {
  project_id: string;
  current_step: number;
  steps: WizardStep[];
  readiness: WizardReadiness;
  step_payloads: Record<string, Record<string, unknown>>;
};

export type WizardStepSaveResponse = {
  project_id: string;
  step_code: string;
  saved: boolean;
  payload: Record<string, unknown>;
};

export type WizardStepValidationResult = {
  step_code: string;
  valid: boolean;
  message: string;
  validations: WizardValidation[];
};
