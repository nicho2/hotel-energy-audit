export type AssumptionSource = "configured" | "defaulted" | "calculated";

export type AssumptionItem = {
  key: string;
  label: string;
  value: string;
  source: AssumptionSource;
  note: string | null;
  warning: boolean;
};

export type AssumptionSection = {
  key: string;
  title: string;
  items: AssumptionItem[];
};

export type ProjectAssumptions = {
  project_id: string;
  calculation_run_id: string | null;
  scenario_name: string | null;
  engine_version: string;
  generated_at: string | null;
  warnings: string[];
  sections: AssumptionSection[];
};
