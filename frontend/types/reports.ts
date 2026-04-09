export type ReportStatus = "pending" | "generated" | "failed";
export type ReportType = "executive" | "detailed";

export type GeneratedReportResponse = {
  id: string;
  organization_id: string;
  project_id: string;
  scenario_id: string;
  calculation_run_id: string;
  branding_profile_id: string | null;
  report_type: ReportType;
  status: ReportStatus | string;
  title: string;
  file_name: string;
  mime_type: string;
  file_size_bytes: number;
  generator_version: string;
  created_at: string;
};

export type CalculationResultLatestResponse = {
  calculation_run_id: string;
  project_id: string;
  scenario_id: string;
  status: string;
  engine_version: string;
  summary: {
    baseline_energy_kwh_year: number;
    scenario_energy_kwh_year: number;
    energy_savings_percent: number;
    baseline_bacs_class: string | null;
    scenario_bacs_class: string | null;
  };
  economic: {
    total_capex: number;
    annual_cost_savings: number;
    simple_payback_years: number;
    npv: number;
    irr: number;
  };
  messages: string[];
  warnings: string[];
  input_snapshot: Record<string, unknown>;
};
