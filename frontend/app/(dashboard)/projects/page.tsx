"use client";

import Link from "next/link";
import { ProjectListTable } from "@/features/projects/components/project-list-table";
import { Button } from "@/components/ui/button";
import { useI18n } from "@/providers/i18n-provider";

export default function ProjectsPage() {
  const { t } = useI18n();

  return (
    <div style={{ display: "grid", gap: 24 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <h1 style={{ fontSize: 32, fontWeight: 600 }}>{t("projects.title")}</h1>
        <Link href="/projects/new">
          <Button>{t("projects.newButton")}</Button>
        </Link>
      </div>
      <ProjectListTable />
    </div>
  );
}
