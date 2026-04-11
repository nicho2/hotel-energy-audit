"use client";

import Link from "next/link";
import { useProject } from "@/features/projects/hooks/use-project";
import { useI18n } from "@/providers/i18n-provider";
import { FeedbackBlock } from "@/components/ui/feedback";
import { ProjectSectionNav } from "@/features/projects/components/project-section-nav";
import { useProjectHistory } from "../hooks/use-project-history";
import { ProjectHistoryTable } from "./project-history-table";

type ProjectHistoryPageProps = {
  projectId: string;
};

export function ProjectHistoryPage({ projectId }: ProjectHistoryPageProps) {
  const { t } = useI18n();
  const project = useProject(projectId);
  const history = useProjectHistory(projectId);

  if (project.isLoading || history.isLoading) {
    return <FeedbackBlock>{t("history.loading")}</FeedbackBlock>;
  }

  if (project.error || history.error) {
    return (
      <FeedbackBlock tone="error">
        {t("history.error")}
      </FeedbackBlock>
    );
  }

  return (
    <div style={{ display: "grid", gap: 20 }}>
      <ProjectSectionNav projectId={projectId} />
      <div style={{ display: "flex", justifyContent: "space-between", gap: 16, alignItems: "flex-start" }}>
        <div style={{ display: "grid", gap: 6 }}>
          <div style={{ fontSize: 13, color: "#627084", textTransform: "uppercase", letterSpacing: 0 }}>
            {t("history.eyebrow")}
          </div>
          <h1 style={{ margin: 0, fontSize: 30, fontWeight: 700 }}>
            {project.data?.data.name ?? t("history.projectFallback")}
          </h1>
          <p style={{ margin: 0, color: "#627084", maxWidth: 760 }}>
            {t("history.description")}
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
          {t("history.backToProject")}
        </Link>
      </div>

      <ProjectHistoryTable events={history.data?.data ?? []} />
    </div>
  );
}
