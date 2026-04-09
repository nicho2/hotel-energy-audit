import { z } from "zod";

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
  quantity: z.string().trim(),
  unit_cost_override: z.string().trim(),
  capex_override: z.string().trim(),
  maintenance_override: z.string().trim(),
  gain_override_percent: z.string().trim(),
  notes: z.string(),
  is_selected: z.boolean(),
});

export type ScenarioEditorFormValues = z.infer<typeof scenarioEditorSchema>;
export type ScenarioSolutionFormValues = z.infer<typeof scenarioSolutionSchema>;
