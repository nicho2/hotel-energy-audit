"use client";

import { useMemo, useState } from "react";
import { ApiError } from "@/lib/api-client/errors";
import { useProject } from "@/features/projects/hooks/use-project";
import { useScenarios } from "@/features/scenarios/hooks/use-scenarios";
import { useScenarioComparison } from "../hooks/use-scenario-comparison";
import { formatCo2, formatCurrency, formatEnergy, formatPercent } from "../utils/formatters";
import { useI18n } from "@/providers/i18n-provider";
import { FeedbackBlock } from "@/components/ui/feedback";
import { ProjectSectionNav } from "@/features/projects/components/project-section-nav";

function toggleSelection(current: string[], scenarioId: string) {
  return current.includes(scenarioId)
    ? current.filter((item) => item !== scenarioId)
    : [...current, scenarioId];
}

export function ComparePage({ projectId }: { projectId: string }) {
  const project = useProject(projectId);
  const scenarios = useScenarios(projectId, null);
  const comparison = useScenarioComparison(projectId);
  const { t } = useI18n();
  const [selectedScenarioIds, setSelectedScenarioIds] = useState<string[]>([]);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const scenarioList = scenarios.scenarios.data?.data ?? [];
  const comparisonData = comparison.data?.data ?? null;

  const recommendedScenarioId = comparisonData?.recommended_scenario.scenario_id ?? null;
  const topEnergy = useMemo(
    () => Math.max(...(comparisonData?.items.map((item) => item.scenario_energy_kwh_year) ?? [0])),
    [comparisonData?.items],
  );

  const summary = useMemo(() => {
    if (!comparisonData || comparisonData.items.length === 0) {
      return null;
    }

    const recommended = comparisonData.items.find((item) => item.scenario_id === recommendedScenarioId) ?? comparisonData.items[0];
    const lowestEnergy = [...comparisonData.items].sort((left, right) => left.scenario_energy_kwh_year - right.scenario_energy_kwh_year)[0];
    const highestROI = [...comparisonData.items].sort((left, right) => right.roi_percent - left.roi_percent)[0];

    return { recommended, lowestEnergy, highestROI };
  }, [comparisonData, recommendedScenarioId]);

  const handleCompare = async () => {
    setSubmitError(null);
    try {
      await comparison.mutateAsync(selectedScenarioIds);
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("compare.error"));
    }
  };

  if (project.isLoading || scenarios.scenarios.isLoading) {
    return <FeedbackBlock>{t("compare.loading")}</FeedbackBlock>;
  }

  return (
    <div style={{ display: "grid", gap: 20 }}>
      <ProjectSectionNav projectId={projectId} />
      <div style={{ display: "grid", gap: 6 }}>
        <div style={{ fontSize: 13, color: "#627084", textTransform: "uppercase", letterSpacing: 0 }}>{t("compare.title")}</div>
        <h1 style={{ margin: 0, fontSize: 30, fontWeight: 700 }}>
          {project.data?.data.name ?? t("compare.projectFallback")}
        </h1>
      </div>

      <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 20, display: "grid", gap: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", gap: 12, alignItems: "center" }}>
          <div style={{ display: "grid", gap: 4 }}>
            <div style={{ fontSize: 18, fontWeight: 700 }}>{t("compare.selectorTitle")}</div>
            <div style={{ color: "#627084", fontSize: 14 }}>
              {t("compare.selectorHelp")}
            </div>
          </div>
          <button
            type="button"
            onClick={handleCompare}
            disabled={selectedScenarioIds.length < 2 || selectedScenarioIds.length > 5 || comparison.isPending}
            style={{
              borderRadius: 10,
              border: "1px solid #14365d",
              background: "#14365d",
              color: "#fff",
              padding: "10px 14px",
              fontWeight: 700,
              cursor: comparison.isPending ? "not-allowed" : "pointer",
              opacity: selectedScenarioIds.length < 2 || selectedScenarioIds.length > 5 || comparison.isPending ? 0.65 : 1,
            }}
          >
            {comparison.isPending ? t("compare.comparing") : t("compare.compare")}
          </button>
        </div>

        {scenarioList.length === 0 ? (
          <FeedbackBlock compact>{t("compare.emptyScenarios")}</FeedbackBlock>
        ) : (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 12 }}>
            {scenarioList.map((scenario) => {
              const selected = selectedScenarioIds.includes(scenario.id);
              const disabled = !selected && selectedScenarioIds.length >= 5;
              return (
                <label
                  key={scenario.id}
                  style={{
                    border: `1px solid ${selected ? "#14365d" : "#e5e7eb"}`,
                    background: selected ? "#eff6ff" : "#fff",
                    borderRadius: 8,
                    padding: 14,
                    display: "grid",
                    gap: 6,
                    opacity: disabled ? 0.6 : 1,
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                    <span style={{ fontWeight: 700 }}>{scenario.name}</span>
                    {scenario.is_reference ? <span style={{ fontSize: 12, color: "#14365d", fontWeight: 700 }}>{t("common.reference")}</span> : null}
                  </div>
                  <div style={{ fontSize: 13, color: "#627084" }}>{scenario.scenario_type} · {scenario.status}</div>
                  <input
                    type="checkbox"
                    checked={selected}
                    disabled={disabled}
                    onChange={() => setSelectedScenarioIds((current) => toggleSelection(current, scenario.id))}
                  />
                </label>
              );
            })}
          </div>
        )}
      </section>

      {submitError ? (
        <FeedbackBlock tone="error" compact>
          {submitError}
        </FeedbackBlock>
      ) : null}

      {!comparisonData ? (
        <section style={{ border: "1px dashed #cbd5e1", borderRadius: 8, padding: 24, textAlign: "center", color: "#627084" }}>
          {t("compare.emptyResults")}
        </section>
      ) : (
        <>
          {summary ? (
            <section style={{ border: "1px solid #bbf7d0", borderRadius: 8, padding: 20, background: "#f0fdf4", display: "grid", gap: 10 }}>
              <div style={{ fontSize: 18, fontWeight: 700, color: "#166534" }}>
                {t("compare.recommendedScenario", { name: comparisonData.recommended_scenario.scenario_name })}
              </div>
              {comparisonData.recommended_scenario.reasons.map((reason) => (
                <div key={reason} style={{ color: "#166534" }}>{reason}</div>
              ))}
            </section>
          ) : null}

          {summary ? (
            <section style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 12 }}>
              <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, display: "grid", gap: 6 }}>
                <div style={{ fontSize: 12, color: "#627084", textTransform: "uppercase" }}>{t("compare.summary.recommended")}</div>
                <div style={{ fontSize: 20, fontWeight: 800 }}>{summary.recommended.scenario_name}</div>
                <div>{formatPercent(summary.recommended.roi_percent)}</div>
              </div>
              <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, display: "grid", gap: 6 }}>
                <div style={{ fontSize: 12, color: "#627084", textTransform: "uppercase" }}>{t("compare.summary.lowestEnergy")}</div>
                <div style={{ fontSize: 20, fontWeight: 800 }}>{summary.lowestEnergy.scenario_name}</div>
                <div>{formatEnergy(summary.lowestEnergy.scenario_energy_kwh_year)}</div>
              </div>
              <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, display: "grid", gap: 6 }}>
                <div style={{ fontSize: 12, color: "#627084", textTransform: "uppercase" }}>{t("compare.summary.highestRoi")}</div>
                <div style={{ fontSize: 20, fontWeight: 800 }}>{summary.highestROI.scenario_name}</div>
                <div>{formatPercent(summary.highestROI.roi_percent)}</div>
              </div>
            </section>
          ) : null}

          <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 20, display: "grid", gap: 16 }}>
            <div style={{ fontSize: 18, fontWeight: 700 }}>{t("compare.energyChart")}</div>
            <div style={{ display: "grid", gap: 12 }}>
              {comparisonData.items.map((item) => (
                <div key={item.scenario_id} style={{ display: "grid", gap: 6 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", gap: 12, fontSize: 14 }}>
                    <span>
                      {item.scenario_name}
                      {item.scenario_id === recommendedScenarioId ? t("compare.recommendedSuffix") : ""}
                    </span>
                    <span>{formatEnergy(item.scenario_energy_kwh_year)}</span>
                  </div>
                  <div style={{ height: 12, borderRadius: 999, background: "#e2e8f0", overflow: "hidden" }}>
                    <div
                      style={{
                        width: `${topEnergy > 0 ? (item.scenario_energy_kwh_year / topEnergy) * 100 : 0}%`,
                        height: "100%",
                        background: item.scenario_id === recommendedScenarioId ? "#16a34a" : "#14365d",
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, overflow: "hidden" }}>
            <div style={{ padding: 20, borderBottom: "1px solid #e5e7eb", fontSize: 18, fontWeight: 700 }}>{t("compare.matrix")}</div>
            <div style={{ overflowX: "auto" }}>
              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr style={{ background: "#f8fafc", textAlign: "left" }}>
                    {[
                      t("compare.headers.scenario"),
                      t("compare.headers.energy"),
                      t("compare.headers.co2"),
                      t("compare.headers.bacs"),
                      t("compare.headers.capex"),
                      t("compare.headers.annualSavings"),
                      t("compare.headers.roi"),
                      t("compare.headers.payback"),
                      t("compare.headers.score"),
                    ].map((label) => (
                      <th key={label} style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 13, fontWeight: 700 }}>
                        {label}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {comparisonData.items.map((item) => (
                    <tr key={item.scenario_id} style={{ background: item.scenario_id === recommendedScenarioId ? "#f0fdf4" : "#fff" }}>
                      <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>
                        <div style={{ display: "grid", gap: 4 }}>
                          <div style={{ fontWeight: 700 }}>{item.scenario_name}</div>
                          <div style={{ fontSize: 13, color: "#627084" }}>{item.is_reference ? t("common.reference") : item.engine_version}</div>
                        </div>
                      </td>
                      <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{formatEnergy(item.scenario_energy_kwh_year)}</td>
                      <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{formatCo2(item.estimated_co2_kg_year)}</td>
                      <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{item.scenario_bacs_class ?? "-"}</td>
                      <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{formatCurrency(item.total_capex)}</td>
                      <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{formatCurrency(item.annual_cost_savings)}</td>
                      <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{formatPercent(item.roi_percent)}</td>
                      <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{t("compare.years", { value: item.simple_payback_years.toFixed(1) })}</td>
                      <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontWeight: 700 }}>{item.score.toFixed(1)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </>
      )}
    </div>
  );
}
