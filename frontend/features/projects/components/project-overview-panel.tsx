"use client";

import { ProjectHeader } from "./project-header";
import { ProjectOverviewCards } from "./project-overview-cards";
import { ProjectSectionNav } from "./project-section-nav";
import { FeedbackBlock } from "@/components/ui/feedback";
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
      <FeedbackBlock>
        {t("projects.loadingProject")}
      </FeedbackBlock>
    );
  }

  if (error) {
    return (
      <FeedbackBlock tone="error">
        {t("projects.projectError")}
      </FeedbackBlock>
    );
  }

  const project = data?.data;

  if (!project) {
    return (
      <FeedbackBlock>
        {t("projects.notFound")}
      </FeedbackBlock>
    );
  }

  return (
    <div style={{ display: "grid", gap: 24 }}>
      <ProjectHeader project={project} />
      <ProjectSectionNav projectId={project.id} />
      <ProjectOverviewCards cards={buildOverviewCards(project.wizard_step, t)} />
    </div>
  );
}
