import { z } from "zod";

const optionalNumberString = z
  .string()
  .trim()
  .refine((value) => value === "" || Number.isFinite(Number(value)), "Veuillez saisir un nombre valide.");

const optionalRatioString = optionalNumberString.refine((value) => {
  if (value === "") {
    return true;
  }
  const numberValue = Number(value);
  return numberValue >= 0 && numberValue <= 1;
}, "Le gain doit etre compris entre 0 et 1.");

export const scenarioEditorSchema = z.object({
  name: z.string().trim().min(1, "Le nom est requis.").max(255, "Le nom est trop long."),
  description: z.string(),
  scenario_type: z.enum(["baseline", "improved", "target_bacs", "custom"]),
  status: z.enum(["draft", "ready", "archived"]),
  is_reference: z.boolean(),
});

export const scenarioSolutionSchema = z.object({
  target_scope: z.enum(["project", "zone", "system"]),
  target_zone_id: z.string(),
  target_system_id: z.string(),
  quantity: optionalNumberString,
  unit_cost_override: optionalNumberString,
  capex_override: optionalNumberString,
  maintenance_override: optionalNumberString,
  gain_override_percent: optionalRatioString,
  notes: z.string(),
  is_selected: z.boolean(),
});

export type ScenarioEditorFormValues = z.infer<typeof scenarioEditorSchema>;
export type ScenarioSolutionFormValues = z.infer<typeof scenarioSolutionSchema>;
