"use client";

import type { BacsSummaryResponse } from "@/types/bacs";
import { useI18n } from "@/providers/i18n-provider";

const classColors: Record<string, { border: string; background: string; color: string }> = {
  A: { border: "#22c55e", background: "#f0fdf4", color: "#166534" },
  B: { border: "#84cc16", background: "#f7fee7", color: "#3f6212" },
  C: { border: "#facc15", background: "#fefce8", color: "#854d0e" },
  D: { border: "#fb923c", background: "#fff7ed", color: "#9a3412" },
  E: { border: "#f87171", background: "#fef2f2", color: "#b91c1c" },
};

type BacsSummaryCardProps = {
  summary: BacsSummaryResponse;
};

export function BacsSummaryCard({ summary }: BacsSummaryCardProps) {
  const { t } = useI18n();
  const badgeColors = classColors[summary.bacs_class];

  return (
    <section style={{ border: "1px solid #e5e7eb", borderRadius: 16, padding: 20, display: "grid", gap: 16 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
        <div style={{ display: "grid", gap: 4 }}>
          <div style={{ fontSize: 18, fontWeight: 700 }}>{t("wizard.bacs.summaryTitle")}</div>
          <div style={{ fontSize: 14, color: "#627084" }}>
            {t("wizard.bacs.summaryDescription")}
          </div>
        </div>
        <div
          style={{
            borderRadius: 999,
            border: `1px solid ${badgeColors.border}`,
            background: badgeColors.background,
            color: badgeColors.color,
            padding: "8px 14px",
            fontWeight: 800,
            fontSize: 18,
          }}
        >
          {t("wizard.bacs.class", { className: summary.bacs_class })}
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, minmax(0, 1fr))", gap: 12 }}>
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 14 }}>
          <div style={{ fontSize: 12, color: "#627084", textTransform: "uppercase" }}>{t("wizard.bacs.score")}</div>
          <div style={{ fontSize: 24, fontWeight: 800 }}>{summary.overall_score}</div>
        </div>
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 14 }}>
          <div style={{ fontSize: 12, color: "#627084", textTransform: "uppercase" }}>{t("wizard.bacs.confidence")}</div>
          <div style={{ fontSize: 24, fontWeight: 800 }}>{Math.round(summary.confidence_score * 100)}%</div>
        </div>
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 14 }}>
          <div style={{ fontSize: 12, color: "#627084", textTransform: "uppercase" }}>{t("wizard.bacs.selectedFunctions")}</div>
          <div style={{ fontSize: 24, fontWeight: 800 }}>
            {summary.selected_function_count}/{summary.total_function_count}
          </div>
        </div>
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 14 }}>
          <div style={{ fontSize: 12, color: "#627084", textTransform: "uppercase" }}>{t("wizard.bacs.estimatedClass")}</div>
          <div style={{ fontSize: 24, fontWeight: 800 }}>
            {summary.estimated_bacs_class}
            {summary.manual_override_class ? ` -> ${summary.manual_override_class}` : ""}
          </div>
        </div>
      </div>

      <div style={{ display: "grid", gap: 10 }}>
        {summary.domain_scores.map((item) => (
          <div key={item.domain} style={{ display: "grid", gap: 6 }}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 14 }}>
              <span>{t(`wizard.bacs.domain.${item.domain}`)}</span>
              <span>{item.score}%</span>
            </div>
            <div style={{ height: 10, borderRadius: 999, background: "#e2e8f0", overflow: "hidden" }}>
              <div style={{ width: `${item.score}%`, height: "100%", background: "#14365d" }} />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
