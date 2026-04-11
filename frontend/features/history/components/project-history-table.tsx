"use client";

import type { ProjectHistoryAction, ProjectHistoryEvent } from "@/types/history";
import { useI18n } from "@/providers/i18n-provider";

type ProjectHistoryTableProps = {
  events: ProjectHistoryEvent[];
};

const badgeStyles: Record<ProjectHistoryAction, { color: string; background: string; border: string }> = {
  project_created: { color: "#14365d", background: "#eff6ff", border: "#bfdbfe" },
  project_updated: { color: "#166534", background: "#f0fdf4", border: "#bbf7d0" },
  scenario_created: { color: "#6d28d9", background: "#f5f3ff", border: "#ddd6fe" },
  scenario_updated: { color: "#92400e", background: "#fffbeb", border: "#fde68a" },
  report_generated: { color: "#0f766e", background: "#f0fdfa", border: "#99f6e4" },
};

function formatDate(value: string, language: string) {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "-";
  }

  return new Intl.DateTimeFormat(language === "en" ? "en-US" : "fr-FR", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

function formatSummary(event: ProjectHistoryEvent, t: (key: string, params?: Record<string, string>) => string) {
  return t(`history.summaries.${event.action}`, { summary: event.summary });
}

export function ProjectHistoryTable({ events }: ProjectHistoryTableProps) {
  const { language, t } = useI18n();

  if (events.length === 0) {
    return (
      <section style={{ border: "1px dashed #cbd5e1", borderRadius: 16, padding: 24, textAlign: "center", color: "#627084" }}>
        {t("history.empty")}
      </section>
    );
  }

  return (
    <section style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", overflow: "hidden" }}>
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
          <thead>
            <tr style={{ background: "#f8fafc", textAlign: "left" }}>
              <th style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{t("history.table.action")}</th>
              <th style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{t("history.table.summary")}</th>
              <th style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{t("history.table.actor")}</th>
              <th style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{t("history.table.time")}</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event, index) => {
              const badge = badgeStyles[event.action];
              return (
                <tr key={`${event.action}-${event.occurred_at}-${index}`}>
                  <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", whiteSpace: "nowrap" }}>
                    <span
                      style={{
                        display: "inline-flex",
                        padding: "4px 8px",
                        borderRadius: 8,
                        border: `1px solid ${badge.border}`,
                        color: badge.color,
                        background: badge.background,
                        fontSize: 12,
                        fontWeight: 700,
                      }}
                    >
                      {t(`history.actions.${event.action}`)}
                    </span>
                  </td>
                  <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", color: "#142033" }}>
                    {formatSummary(event, t)}
                  </td>
                  <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", color: "#627084" }}>
                    {event.actor}
                  </td>
                  <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", color: "#627084", whiteSpace: "nowrap" }}>
                    {formatDate(event.occurred_at, language)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}
