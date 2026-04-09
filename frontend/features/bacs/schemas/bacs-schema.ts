import { z } from "zod";

export const bacsStepSchema = z.object({
  assessor_name: z.string().trim().max(255, "Le nom est trop long."),
  manual_override_class: z.union([z.enum(["A", "B", "C", "D", "E"]), z.literal("")]),
  notes: z.string(),
  selected_function_ids: z.array(z.string().uuid()).default([]),
});

export type BacsStepFormValues = z.infer<typeof bacsStepSchema>;
