"use client";

import { CreateProjectForm } from "@/features/projects/components/create-project-form";
import { useI18n } from "@/providers/i18n-provider";

export default function NewProjectPage() {
  const { t } = useI18n();

  return (
    <div style={{ display: "grid", gap: 24 }}>
      <div style={{ display: "grid", gap: 8 }}>
        <h1 style={{ fontSize: 32, fontWeight: 600, margin: 0 }}>{t("projects.newTitle")}</h1>
        <p style={{ margin: 0, color: "#627084", maxWidth: 720 }}>
          {t("projects.newDescription")}
        </p>
      </div>
      <CreateProjectForm />
    </div>
  );
}
