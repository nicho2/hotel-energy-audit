export type BacsDomain = "monitoring" | "heating" | "cooling_ventilation" | "dhw" | "lighting";
export type BacsClass = "A" | "B" | "C" | "D" | "E";

export type BacsFunctionResponse = {
  id: string;
  code: string;
  domain: BacsDomain;
  name: string;
  description: string | null;
  weight: number;
  order_index: number;
  is_selected: boolean;
};

export type BacsCurrentResponse = {
  assessment_id: string | null;
  project_id: string;
  version: string;
  assessor_name: string | null;
  manual_override_class: BacsClass | null;
  notes: string | null;
  functions: BacsFunctionResponse[];
};

export type BacsDomainScoreResponse = {
  domain: BacsDomain;
  score: number;
  selected_weight: number;
  total_weight: number;
};

export type BacsMissingFunctionResponse = {
  id: string;
  code: string;
  domain: BacsDomain;
  name: string;
  description: string | null;
  weight: number;
};

export type BacsSummaryResponse = {
  assessment_id: string | null;
  project_id: string;
  version: string;
  confidence_score: number;
  overall_score: number;
  estimated_bacs_class: BacsClass;
  manual_override_class: BacsClass | null;
  bacs_class: BacsClass;
  selected_function_count: number;
  total_function_count: number;
  domain_scores: BacsDomainScoreResponse[];
  top_missing_functions: BacsMissingFunctionResponse[];
};

export type BacsAssessmentUpsertPayload = {
  assessor_name: string | null;
  manual_override_class: BacsClass | null;
  notes: string | null;
};

export type BacsCurrentFunctionsUpdatePayload = {
  selected_function_ids: string[];
};
