"use client";

import Link from "next/link";
import { useProject } from "@/features/projects/hooks/use-project";
import { useI18n } from "@/providers/i18n-provider";
import { useProjectAssumptions } from "../hooks/use-project-assumptions";
import { AssumptionsSectionCard } from "./assumptions-section-card";

type AssumptionsPageProps = {
  projectId: string;
};

function formatDate(value: string | null, language: string) {
  if (!value) {
    return "-";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "-";
  }

  return new Intl.DateTimeFormat(language === "en" ? "en-US" : "fr-FR", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export function AssumptionsPage({ projectId }: AssumptionsPageProps) {
  const { language, t } = useI18n();
  const project = useProject(projectId);
  const assumptions = useProjectAssumptions(projectId);
  const data = assumptions.data?.data ?? null;

  if (project.isLoading || assumptions.isLoading) {
    return <div>{t("assumptions.loading")}</div>;
  }

  if (project.error || assumptions.error || !data) {
    return (
      <div style={{ border: "1px solid #fecaca", borderRadius: 16, background: "#fff", padding: 24, color: "#b91c1c" }}>
        {t("assumptions.error")}
      </div>
    );
  }

  return (
    <div style={{ display: "grid", gap: 20 }}>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 16, alignItems: "flex-start" }}>
        <div style={{ display: "grid", gap: 6 }}>
          <div style={{ fontSize: 13, color: "#627084", textTransform: "uppercase", letterSpacing: "0.04em" }}>
            {t("assumptions.eyebrow")}
          </div>
          <h1 style={{ margin: 0, fontSize: 30, fontWeight: 700 }}>
            {project.data?.data.name ?? t("assumptions.projectFallback")}
          </h1>
          <p style={{ margin: 0, color: "#627084", maxWidth: 820 }}>
            {t("assumptions.description")}
          </p>
        </div>
        <Link
          href={`/projects/${projectId}`}
          style={{
            display: "inline-flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "10px 14px",
            borderRadius: 8,
            border: "1px solid #d7dee7",
            background: "#fff",
            color: "#142033",
            fontWeight: 600,
            whiteSpace: "nowrap",
          }}
        >
          {t("assumptions.backToProject")}
        </Link>
      </div>

      <section style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 12 }}>
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 12, background: "#fff", padding: 14, display: "grid", gap: 4 }}>
          <div style={{ color: "#627084", fontSize: 12, textTransform: "uppercase" }}>{t("assumptions.meta.engine")}</div>
          <div style={{ fontWeight: 800 }}>{data.engine_version}</div>
        </div>
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 12, background: "#fff", padding: 14, display: "grid", gap: 4 }}>
          <div style={{ color: "#627084", fontSize: 12, textTransform: "uppercase" }}>{t("assumptions.meta.scenario")}</div>
          <div style={{ fontWeight: 800 }}>{data.scenario_name ?? t("assumptions.noCalculation")}</div>
        </div>
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 12, background: "#fff", padding: 14, display: "grid", gap: 4 }}>
          <div style={{ color: "#627084", fontSize: 12, textTransform: "uppercase" }}>{t("assumptions.meta.generatedAt")}</div>
          <div style={{ fontWeight: 800 }}>{formatDate(data.generated_at, language)}</div>
        </div>
      </section>

      {data.warnings.length > 0 ? (
        <section style={{ border: "1px solid #fde68a", borderRadius: 16, background: "#fffbeb", padding: 16, display: "grid", gap: 8 }}>
          <div style={{ color: "#92400e", fontWeight: 800 }}>{t("assumptions.warningsTitle")}</div>
          {data.warnings.map((warning) => (
            <div key={warning} style={{ color: "#92400e", fontSize: 14 }}>
              {warning}
            </div>
          ))}
        </section>
      ) : null}

      <div style={{ display: "grid", gap: 16 }}>
        {data.sections.map((section) => (
          <AssumptionsSectionCard key={section.key} section={section} />
        ))}
      </div>
    </div>
  );
}
