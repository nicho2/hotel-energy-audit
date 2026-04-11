import Link from "next/link";
import type { ProjectResponse } from "@/types/project";
import { BrandingSummary } from "@/features/branding/components/branding-summary";
import { useBrandingProfiles } from "@/features/branding/hooks/use-branding-profiles";
import { getDefaultBrandingProfile } from "@/features/branding/utils/branding";
import { useI18n } from "@/providers/i18n-provider";

const quickLinks = [
  { segment: "wizard", labelKey: "projects.header.openWizard" },
  { segment: "scenarios", labelKey: "projects.header.viewScenarios" },
  { segment: "compare", labelKey: "projects.header.openCompare" },
  { segment: "reports", labelKey: "projects.header.viewReports" },
  { segment: "history", labelKey: "projects.header.viewHistory" },
  { segment: "assumptions", labelKey: "projects.header.viewAssumptions" },
];

type ProjectHeaderProps = {
  project: ProjectResponse;
};

export function ProjectHeader({ project }: ProjectHeaderProps) {
  const { t } = useI18n();
  const brandingProfiles = useBrandingProfiles();
  const profiles = brandingProfiles.data?.data ?? [];
  const projectBranding =
    profiles.find((profile) => profile.id === project.branding_profile_id) ??
    (project.branding_profile_id ? null : getDefaultBrandingProfile(profiles));

  return (
    <div
      style={{
        border: "1px solid #e5e7eb",
        borderRadius: 20,
        background: "#fff",
        padding: 24,
        display: "grid",
        gap: 20,
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", gap: 24, alignItems: "flex-start" }}>
        <div style={{ display: "grid", gap: 8 }}>
          <div style={{ fontSize: 13, color: "#627084" }}>{t("projects.header.label")}</div>
          <h1 style={{ margin: 0, fontSize: 32, fontWeight: 700 }}>{project.name}</h1>
          <div style={{ display: "flex", gap: 12, flexWrap: "wrap", color: "#627084", fontSize: 14 }}>
            <span>{t("projects.header.client")}: {project.client_name ?? t("common.emptyDash")}</span>
            <span>{t("common.status")}: {project.status}</span>
            <span>{t("projects.table.wizardStep")}: {project.wizard_step}</span>
          </div>
        </div>

        <div
          style={{
            padding: "8px 12px",
            borderRadius: 999,
            background: "#f8fafc",
            border: "1px solid #d7dee7",
            color: "#14365d",
            fontSize: 13,
            fontWeight: 600,
          }}
        >
          {project.building_type}
        </div>
      </div>

      <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        {quickLinks.map((link) => (
          <Link
            key={link.segment}
            href={`/projects/${project.id}/${link.segment}`}
            style={{
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "center",
              padding: "10px 14px",
              borderRadius: 10,
              background: "#14365d",
              color: "#fff",
              fontWeight: 600,
            }}
          >
            {t(link.labelKey)}
          </Link>
        ))}
      </div>

      <BrandingSummary profile={projectBranding} isLoading={brandingProfiles.isLoading} />
    </div>
  );
}
