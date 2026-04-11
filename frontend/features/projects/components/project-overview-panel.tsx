"use client";

import { ProjectHeader } from "./project-header";
import { ProjectOverviewCards } from "./project-overview-cards";
import { useProject } from "../hooks/use-project";
import type { ProjectOverviewCard } from "@/types/project";
import { useI18n } from "@/providers/i18n-provider";

function buildOverviewCards(wizardStep: number, t: (key: string, params?: Record<string, string | number>) => string): ProjectOverviewCard[] {
  return [
    {
      key: "energy",
      label: t("projects.overview.energy"),
      value: "--",
      helper: t("projects.overview.energyHelper"),
    },
    {
      key: "co2",
      label: "CO2",
      value: "--",
      helper: t("projects.overview.co2Helper"),
    },
    {
      key: "bacs",
      label: "BACS",
      value: t("projects.overview.stepValue", { step: wizardStep }),
      helper: t("projects.overview.bacsHelper"),
    },
    {
      key: "roi",
      label: "ROI",
      value: "--",
      helper: t("projects.overview.roiHelper"),
    },
  ];
}

type ProjectOverviewPanelProps = {
  projectId: string;
};

export function ProjectOverviewPanel({ projectId }: ProjectOverviewPanelProps) {
  const { data, error, isLoading } = useProject(projectId);
  const { t } = useI18n();

  if (isLoading) {
    return (
      <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 24 }}>
        {t("projects.loadingProject")}
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ border: "1px solid #fecaca", borderRadius: 16, background: "#fff", padding: 24, color: "#b91c1c" }}>
        {t("projects.projectError")}
      </div>
    );
  }

  const project = data?.data;

  if (!project) {
    return (
      <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 24 }}>
        {t("projects.notFound")}
      </div>
    );
  }

  return (
    <div style={{ display: "grid", gap: 24 }}>
      <ProjectHeader project={project} />
      <ProjectOverviewCards cards={buildOverviewCards(project.wizard_step, t)} />
    </div>
  );
}
