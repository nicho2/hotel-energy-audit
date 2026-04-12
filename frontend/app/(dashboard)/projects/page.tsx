"use client";

import Link from "next/link";
import { useState } from "react";
import { ProjectListTable } from "@/features/projects/components/project-list-table";
import { Button } from "@/components/ui/button";
import { useI18n } from "@/providers/i18n-provider";
import { useAuthContext } from "@/providers/auth-provider";
import { useDeleteProjects } from "@/features/projects/hooks/use-delete-projects";
import { ApiError } from "@/lib/api-client/errors";

export default function ProjectsPage() {
  const { t } = useI18n();
  const { user } = useAuthContext();
  const deleteProjects = useDeleteProjects();
  const [selectedProjectIds, setSelectedProjectIds] = useState<string[]>([]);
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const canDeleteProjects = user?.role === "org_admin";

  const handleDeleteSelected = async () => {
    if (!canDeleteProjects || selectedProjectIds.length === 0) {
      return;
    }

    const confirmed = window.confirm(t("projects.delete.confirm", { count: selectedProjectIds.length }));
    if (!confirmed) {
      return;
    }

    setDeleteError(null);
    try {
      await deleteProjects.mutateAsync(selectedProjectIds);
      setSelectedProjectIds([]);
    } catch (error) {
      setDeleteError(error instanceof ApiError ? error.message : t("projects.delete.error"));
    }
  };

  return (
    <div style={{ display: "grid", gap: 24 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <h1 style={{ fontSize: 32, fontWeight: 600 }}>{t("projects.title")}</h1>
        <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
          {canDeleteProjects ? (
            <Button
              type="button"
              disabled={selectedProjectIds.length === 0 || deleteProjects.isPending}
              onClick={handleDeleteSelected}
            >
              {deleteProjects.isPending
                ? t("projects.delete.deleting")
                : t("projects.delete.button", { count: selectedProjectIds.length })}
            </Button>
          ) : null}
          <Link href="/projects/new">
            <Button>{t("projects.newButton")}</Button>
          </Link>
        </div>
      </div>
      {deleteError ? (
        <div style={{ border: "1px solid #fecaca", borderRadius: 8, background: "#fff", padding: 14, color: "#b91c1c" }}>
          {deleteError}
        </div>
      ) : null}
      <ProjectListTable
        selectedProjectIds={selectedProjectIds}
        onSelectedProjectIdsChange={setSelectedProjectIds}
      />
    </div>
  );
}
