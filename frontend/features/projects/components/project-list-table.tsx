"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { useProjects } from "../hooks/use-projects";
import type { ProjectListItem } from "@/types/project";
import { useI18n } from "@/providers/i18n-provider";
import { useAuthContext } from "@/providers/auth-provider";

type SortKey = "name" | "client_name" | "status" | "wizard_step" | "updated_at";
type SortDirection = "asc" | "desc";

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

type ProjectListTableProps = {
  selectedProjectIds: string[];
  onSelectedProjectIdsChange: (projectIds: string[]) => void;
};

export function ProjectListTable({ selectedProjectIds, onSelectedProjectIdsChange }: ProjectListTableProps) {
  const { data, isLoading, error } = useProjects();
  const { language, t } = useI18n();
  const { user } = useAuthContext();
  const [sort, setSort] = useState<{ key: SortKey; direction: SortDirection }>({
    key: "updated_at",
    direction: "desc",
  });
  const canSelectProjects = user?.role === "org_admin";
  const projects = useMemo(() => {
    const items = [...(data?.data ?? [])];
    items.sort((left, right) => compareProjects(left, right, sort.key, sort.direction));
    return items;
  }, [data?.data, sort]);
  const visibleProjectIds = projects.map((project) => project.id);
  const selectedVisibleProjectIds = selectedProjectIds.filter((projectId) => visibleProjectIds.includes(projectId));
  const allVisibleSelected = visibleProjectIds.length > 0 && selectedVisibleProjectIds.length === visibleProjectIds.length;
  const someVisibleSelected = selectedVisibleProjectIds.length > 0 && !allVisibleSelected;

  const toggleSort = (key: SortKey) => {
    setSort((current) => ({
      key,
      direction: current.key === key && current.direction === "asc" ? "desc" : "asc",
    }));
  };

  const toggleAllVisible = () => {
    if (allVisibleSelected) {
      onSelectedProjectIdsChange(selectedProjectIds.filter((projectId) => !visibleProjectIds.includes(projectId)));
      return;
    }

    onSelectedProjectIdsChange(Array.from(new Set([...selectedProjectIds, ...visibleProjectIds])));
  };

  const toggleProject = (projectId: string) => {
    if (selectedProjectIds.includes(projectId)) {
      onSelectedProjectIdsChange(selectedProjectIds.filter((item) => item !== projectId));
      return;
    }

    onSelectedProjectIdsChange([...selectedProjectIds, projectId]);
  };

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
            {canSelectProjects ? (
              <th style={{ padding: 12, width: 44 }}>
                <input
                  type="checkbox"
                  aria-label={t("projects.table.selectAll")}
                  checked={allVisibleSelected}
                  ref={(input) => {
                    if (input) input.indeterminate = someVisibleSelected;
                  }}
                  onChange={toggleAllVisible}
                />
              </th>
            ) : null}
            <SortableHeader label={t("projects.table.project")} sortKey="name" activeSort={sort} onSort={toggleSort} />
            <SortableHeader label={t("projects.table.client")} sortKey="client_name" activeSort={sort} onSort={toggleSort} />
            <SortableHeader label={t("projects.table.status")} sortKey="status" activeSort={sort} onSort={toggleSort} />
            <SortableHeader label={t("projects.table.wizardStep")} sortKey="wizard_step" activeSort={sort} onSort={toggleSort} />
            <SortableHeader label={t("projects.table.updatedAt")} sortKey="updated_at" activeSort={sort} onSort={toggleSort} />
          </tr>
        </thead>
        <tbody>
          {projects.map((project: ProjectListItem) => (
            <tr key={project.id} style={{ borderTop: "1px solid #e5e7eb" }}>
              {canSelectProjects ? (
                <td style={{ padding: 12 }}>
                  <input
                    type="checkbox"
                    aria-label={t("projects.table.selectProject", { name: project.name })}
                    checked={selectedProjectIds.includes(project.id)}
                    onChange={() => toggleProject(project.id)}
                  />
                </td>
              ) : null}
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

function SortableHeader({
  label,
  sortKey,
  activeSort,
  onSort,
}: {
  label: string;
  sortKey: SortKey;
  activeSort: { key: SortKey; direction: SortDirection };
  onSort: (sortKey: SortKey) => void;
}) {
  const isActive = activeSort.key === sortKey;
  const indicator = isActive ? (activeSort.direction === "asc" ? " ^" : " v") : "";

  return (
    <th style={{ padding: 12 }}>
      <button
        type="button"
        onClick={() => onSort(sortKey)}
        style={{
          border: 0,
          background: "transparent",
          padding: 0,
          font: "inherit",
          fontWeight: 700,
          color: "#334155",
          cursor: "pointer",
        }}
      >
        {label}{indicator}
      </button>
    </th>
  );
}

function compareProjects(left: ProjectListItem, right: ProjectListItem, key: SortKey, direction: SortDirection) {
  const multiplier = direction === "asc" ? 1 : -1;

  if (key === "updated_at") {
    return (new Date(left.updated_at).getTime() - new Date(right.updated_at).getTime()) * multiplier;
  }

  if (key === "wizard_step") {
    return (Number(left.wizard_step) - Number(right.wizard_step)) * multiplier;
  }

  const leftValue = String(left[key] ?? "").toLocaleLowerCase();
  const rightValue = String(right[key] ?? "").toLocaleLowerCase();
  return leftValue.localeCompare(rightValue) * multiplier;
}
