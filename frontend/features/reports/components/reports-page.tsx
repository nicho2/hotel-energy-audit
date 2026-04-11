"use client";

import { useEffect, useMemo, useState } from "react";
import { ApiError } from "@/lib/api-client/errors";
import { useProject } from "@/features/projects/hooks/use-project";
import type { GeneratedReportResponse } from "@/types/reports";
import { downloadGeneratedReport } from "../api/download-generated-report";
import { ReportGeneratorForm } from "./report-generator-form";
import { ReportHistoryTable } from "./report-history-table";
import { useReports } from "../hooks/use-reports";
import type { ReportGeneratorFormValues } from "../schemas/report-generator-schema";
import { useI18n } from "@/providers/i18n-provider";

export function ReportsPage({ projectId }: { projectId: string }) {
  const project = useProject(projectId);
  const { t } = useI18n();
  const [selectedScenarioId, setSelectedScenarioId] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [downloadError, setDownloadError] = useState<string | null>(null);
  const [downloadingReportId, setDownloadingReportId] = useState<string | null>(null);
  const reports = useReports(projectId, selectedScenarioId);

  const scenarioList = reports.scenarios.data?.data ?? [];
  const reportHistory = reports.reports.data?.data ?? [];
  const latestResult = reports.latestResult.data?.data ?? null;

  useEffect(() => {
    if (!selectedScenarioId && scenarioList[0]) {
      setSelectedScenarioId(scenarioList[0].id);
    }
  }, [scenarioList, selectedScenarioId]);

  const scenarioNames = useMemo(
    () => new Map(scenarioList.map((scenario) => [scenario.id, scenario.name])),
    [scenarioList],
  );

  const handleGenerate = async (_values: ReportGeneratorFormValues) => {
    if (!latestResult) {
      return;
    }

    setSubmitError(null);
    try {
      await reports.generateReport.mutateAsync(latestResult.calculation_run_id);
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("reports.generateError"));
    }
  };

  const handleDownload = async (report: GeneratedReportResponse) => {
    if (!reports.token) {
      setDownloadError(t("reports.noSessionDownload"));
      return;
    }

    setDownloadError(null);
    setDownloadingReportId(report.id);
    try {
      await downloadGeneratedReport(report.id, reports.token, report.file_name);
    } catch (error) {
      setDownloadError(error instanceof Error ? error.message : t("reports.downloadError"));
    } finally {
      setDownloadingReportId(null);
    }
  };

  if (project.isLoading || reports.scenarios.isLoading || reports.reports.isLoading) {
    return <div>{t("reports.loading")}</div>;
  }

  return (
    <div style={{ display: "grid", gap: 20 }}>
      <div style={{ display: "grid", gap: 6 }}>
        <div style={{ fontSize: 13, color: "#627084", textTransform: "uppercase", letterSpacing: "0.04em" }}>{t("reports.title")}</div>
        <h1 style={{ margin: 0, fontSize: 30, fontWeight: 700 }}>{project.data?.data.name ?? t("reports.projectFallback")}</h1>
      </div>

      {submitError ? (
        <div style={{ border: "1px solid #fecaca", borderRadius: 12, background: "#fff", padding: 16, color: "#b91c1c" }}>
          {submitError}
        </div>
      ) : null}

      {downloadError ? (
        <div style={{ border: "1px solid #fecaca", borderRadius: 12, background: "#fff", padding: 16, color: "#b91c1c" }}>
          {downloadError}
        </div>
      ) : null}

      {scenarioList.length === 0 ? (
        <section style={{ border: "1px dashed #cbd5e1", borderRadius: 16, padding: 24, textAlign: "center", color: "#627084" }}>
          {t("reports.noScenario")}
        </section>
      ) : (
        <ReportGeneratorForm
          project={project.data?.data ?? null}
          scenarios={scenarioList}
          selectedScenarioId={selectedScenarioId}
          latestResult={latestResult}
          isLoadingLatestResult={reports.latestResult.isLoading}
          isGenerating={reports.generateReport.isPending}
          onScenarioChange={setSelectedScenarioId}
          onSubmit={handleGenerate}
        />
      )}

      <ReportHistoryTable
        reports={reportHistory}
        scenarioNames={scenarioNames}
        onDownload={handleDownload}
        isDownloadingReportId={downloadingReportId}
      />
    </div>
  );
}
