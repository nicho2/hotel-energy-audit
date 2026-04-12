import { z } from "zod";

export const wizardDraftStepSchema = z.record(
  z.union([z.string(), z.number(), z.boolean(), z.array(z.string()), z.null()]),
);

export type WizardDraftStepValues = z.infer<typeof wizardDraftStepSchema>;
