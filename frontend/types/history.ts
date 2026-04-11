export type ProjectHistoryAction =
  | "project_created"
  | "project_updated"
  | "scenario_created"
  | "scenario_updated"
  | "report_generated";

export type ProjectHistoryEvent = {
  action: ProjectHistoryAction;
  actor: string;
  occurred_at: string;
  summary: string;
};
