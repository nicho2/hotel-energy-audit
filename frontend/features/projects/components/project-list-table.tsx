"use client";

import Link from "next/link";
import { useProjects } from "../hooks/use-projects";
import type { ProjectListItem } from "@/types/project";
import { useI18n } from "@/providers/i18n-provider";

function formatUpdatedAt(value: string, language: string) {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "-";
  }

  return new Intl.DateTimeFormat(language === "en" ? "en-US" : "fr-FR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(date);
}

export function ProjectListTable() {
  const { data, isLoading, error } = useProjects();
  const { language, t } = useI18n();

  if (isLoading) {
    return (
      <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 24 }}>
        {t("projects.loadingList")}
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ border: "1px solid #fecaca", borderRadius: 16, background: "#fff", padding: 24, color: "#b91c1c" }}>
        {t("projects.listError")}
      </div>
    );
  }

  const projects = data?.data ?? [];

  if (projects.length === 0) {
    return (
      <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 24 }}>
        {t("projects.empty")}
      </div>
    );
  }

  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", overflow: "hidden" }}>
      <table style={{ width: "100%", fontSize: 14, borderCollapse: "collapse" }}>
        <thead style={{ background: "#f9fafb", textAlign: "left" }}>
          <tr>
            <th style={{ padding: 12 }}>{t("projects.table.project")}</th>
            <th style={{ padding: 12 }}>{t("projects.table.client")}</th>
            <th style={{ padding: 12 }}>{t("projects.table.status")}</th>
            <th style={{ padding: 12 }}>{t("projects.table.wizardStep")}</th>
            <th style={{ padding: 12 }}>{t("projects.table.updatedAt")}</th>
          </tr>
        </thead>
        <tbody>
          {projects.map((project: ProjectListItem) => (
            <tr key={project.id} style={{ borderTop: "1px solid #e5e7eb" }}>
              <td style={{ padding: 12 }}>
                <Link href={`/projects/${project.id}`}>{project.name}</Link>
              </td>
              <td style={{ padding: 12 }}>{project.client_name ?? t("common.emptyDash")}</td>
              <td style={{ padding: 12 }}>{project.status}</td>
              <td style={{ padding: 12 }}>{project.wizard_step}</td>
              <td style={{ padding: 12 }}>{formatUpdatedAt(project.updated_at, language)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
