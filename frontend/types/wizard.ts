export type WizardStep = {
  code: string;
  label: string;
  status: string;
};

export type WizardState = {
  current_step: number | string;
  steps: WizardStep[];
};
