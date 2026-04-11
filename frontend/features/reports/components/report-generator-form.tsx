"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import type { ProjectResponse } from "@/types/project";
import type { CalculationResultLatestResponse } from "@/types/reports";
import type { ScenarioResponse } from "@/types/scenarios";
import {
  reportGeneratorSchema,
  type ReportGeneratorFormValues,
} from "../schemas/report-generator-schema";
import { useI18n } from "@/providers/i18n-provider";

const inputStyle = {
  width: "100%",
  borderRadius: 8,
  border: "1px solid #d1d5db",
  padding: "10px 12px",
  fontSize: 14,
  background: "#fff",
} as const;

type ReportGeneratorFormProps = {
  project: ProjectResponse | null;
  scenarios: ScenarioResponse[];
  selectedScenarioId: string | null;
  latestResult: CalculationResultLatestResponse | null;
  isLoadingLatestResult: boolean;
  isGenerating: boolean;
  onScenarioChange: (scenarioId: string) => void;
  onSubmit: (values: ReportGeneratorFormValues) => void;
};

export function ReportGeneratorForm({
  project,
  scenarios,
  selectedScenarioId,
  latestResult,
  isLoadingLatestResult,
  isGenerating,
  onScenarioChange,
  onSubmit,
}: ReportGeneratorFormProps) {
  const { t } = useI18n();
  const form = useForm<ReportGeneratorFormValues>({
    resolver: zodResolver(reportGeneratorSchema),
    defaultValues: {
      scenario_id: selectedScenarioId ?? "",
      report_type: "executive",
    },
  });

  useEffect(() => {
    form.setValue("scenario_id", selectedScenarioId ?? "");
  }, [form, selectedScenarioId]);

  const handleSubmit = form.handleSubmit(onSubmit);

  return (
    <section style={{ border: "1px solid #e5e7eb", borderRadius: 16, padding: 20, display: "grid", gap: 16 }}>
      <div style={{ display: "grid", gap: 4 }}>
        <div style={{ fontSize: 20, fontWeight: 700 }}>{t("reports.generatorTitle")}</div>
        <div style={{ color: "#627084", fontSize: 14 }}>
          {t("reports.generatorHelp")}
        </div>
      </div>

      <form onSubmit={handleSubmit} style={{ display: "grid", gap: 16 }}>
        <div style={{ display: "grid", gridTemplateColumns: "1.4fr 0.8fr", gap: 12 }}>
          <label style={{ display: "grid", gap: 8 }}>
            <span style={{ fontSize: 13, fontWeight: 700, color: "#334155" }}>{t("reports.scenario")}</span>
            <select
              {...form.register("scenario_id")}
              style={inputStyle}
              onChange={(event) => {
                form.setValue("scenario_id", event.target.value);
                onScenarioChange(event.target.value);
              }}
            >
              <option value="">{t("reports.selectScenario")}</option>
              {scenarios.map((scenario) => (
                <option key={scenario.id} value={scenario.id}>
                  {scenario.name}
                </option>
              ))}
            </select>
          </label>

          <label style={{ display: "grid", gap: 8 }}>
            <span style={{ fontSize: 13, fontWeight: 700, color: "#334155" }}>{t("reports.reportType")}</span>
            <select {...form.register("report_type")} style={inputStyle} disabled>
              <option value="executive">executive</option>
            </select>
          </label>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 12 }}>
          <div style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 14, display: "grid", gap: 4 }}>
            <div style={{ fontSize: 12, color: "#627084", textTransform: "uppercase" }}>{t("reports.branding")}</div>
            <div style={{ fontWeight: 700 }}>{project?.branding_profile_id ? t("reports.projectProfile") : t("reports.fallbackBranding")}</div>
            <div style={{ fontSize: 13, color: "#627084" }}>{t("reports.brandingHelp")}</div>
          </div>
          <div style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 14, display: "grid", gap: 4 }}>
            <div style={{ fontSize: 12, color: "#627084", textTransform: "uppercase" }}>{t("reports.language")}</div>
            <div style={{ fontWeight: 700 }}>{t("reports.defaultBackend")}</div>
            <div style={{ fontSize: 13, color: "#627084" }}>{t("reports.languageHelp")}</div>
          </div>
          <div style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 14, display: "grid", gap: 4 }}>
            <div style={{ fontSize: 12, color: "#627084", textTransform: "uppercase" }}>{t("reports.calculation")}</div>
            <div style={{ fontWeight: 700 }}>
              {isLoadingLatestResult ? t("reports.searching") : latestResult ? t("reports.latestAvailable") : t("reports.missing")}
            </div>
            <div style={{ fontSize: 13, color: "#627084" }}>
              {latestResult ? latestResult.calculation_run_id : t("reports.calculateFirst")}
            </div>
          </div>
        </div>

        {latestResult ? (
          <div style={{ border: "1px solid #dbeafe", background: "#eff6ff", borderRadius: 12, padding: 14, display: "grid", gap: 6 }}>
            <div style={{ fontWeight: 700, color: "#1d4ed8" }}>{t("reports.latestCalculation")}</div>
            <div style={{ fontSize: 14, color: "#1e3a8a" }}>Engine: {latestResult.engine_version}</div>
            <div style={{ fontSize: 14, color: "#1e3a8a" }}>Status: {latestResult.status}</div>
          </div>
        ) : (
          <div style={{ border: "1px solid #fecaca", background: "#fff", color: "#b91c1c", borderRadius: 12, padding: 14 }}>
            {t("reports.noCalculation")}
          </div>
        )}

        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <button
            type="submit"
            disabled={!latestResult || isGenerating}
            style={{
              borderRadius: 10,
              border: "1px solid #14365d",
              background: "#14365d",
              color: "#fff",
              padding: "10px 14px",
              fontWeight: 700,
              cursor: !latestResult || isGenerating ? "not-allowed" : "pointer",
              opacity: !latestResult || isGenerating ? 0.7 : 1,
            }}
          >
            {isGenerating ? t("reports.generating") : t("reports.generate")}
          </button>
        </div>
      </form>
    </section>
  );
}
