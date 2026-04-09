export type ScenarioComparisonItem = {
  scenario_id: string;
  scenario_name: string;
  calculation_run_id: string;
  is_reference: boolean;
  engine_version: string;
  scenario_energy_kwh_year: number;
  estimated_co2_kg_year: number;
  baseline_bacs_class: string | null;
  scenario_bacs_class: string | null;
  total_capex: number;
  annual_cost_savings: number;
  simple_payback_years: number;
  roi_percent: number;
  score: number;
};

export type ScenarioComparisonRecommendation = {
  scenario_id: string;
  scenario_name: string;
  score: number;
  reasons: string[];
};

export type ScenarioComparisonResponse = {
  project_id: string;
  compared_scenario_ids: string[];
  items: ScenarioComparisonItem[];
  recommended_scenario: ScenarioComparisonRecommendation;
};
