export type ScenarioType = "baseline" | "improved" | "target_bacs" | "custom";
export type ScenarioStatus = "draft" | "ready" | "archived";
export type TargetScope = "project" | "zone" | "system";

export type ScenarioResponse = {
  id: string;
  project_id: string;
  name: string;
  description: string | null;
  scenario_type: ScenarioType;
  status: ScenarioStatus;
  derived_from_scenario_id: string | null;
  is_reference: boolean;
  created_at: string;
  updated_at: string;
};

export type ScenarioCreatePayload = {
  name: string;
  description: string | null;
  scenario_type: ScenarioType;
  derived_from_scenario_id: string | null;
  is_reference: boolean;
};

export type ScenarioUpdatePayload = Partial<{
  name: string;
  description: string | null;
  scenario_type: ScenarioType;
  status: ScenarioStatus;
  is_reference: boolean;
}>;

export type ScenarioDuplicatePayload = {
  name: string | null;
};

export type SolutionCatalogItem = {
  code: string;
  name: string;
  description: string;
  solution_family: string;
  target_scopes: TargetScope[];
  default_quantity: number | null;
  default_unit: string | null;
};

export type ScenarioSolutionAssignment = {
  id: string;
  scenario_id: string;
  solution_code: string;
  solution_name: string;
  solution_description: string;
  solution_family: string;
  target_scope: TargetScope;
  target_zone_id: string | null;
  target_system_id: string | null;
  quantity: number | null;
  unit_cost_override: number | null;
  capex_override: number | null;
  maintenance_override: number | null;
  gain_override_percent: number | null;
  notes: string | null;
  is_selected: boolean;
  created_at: string;
  updated_at: string;
};

export type ScenarioSolutionAssignmentCreatePayload = {
  solution_code: string;
  target_scope: TargetScope;
  target_zone_id: string | null;
  target_system_id: string | null;
  quantity: number | null;
  unit_cost_override: number | null;
  capex_override: number | null;
  maintenance_override: number | null;
  gain_override_percent: number | null;
  notes: string | null;
  is_selected: boolean;
};

export type ScenarioSolutionAssignmentUpdatePayload = Partial<Omit<ScenarioSolutionAssignmentCreatePayload, "solution_code">>;
