"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useI18n } from "@/providers/i18n-provider";

const sections = [
  { href: "", labelKey: "projects.nav.overview" },
  { href: "wizard", labelKey: "projects.nav.wizard" },
  { href: "scenarios", labelKey: "projects.nav.scenarios" },
  { href: "compare", labelKey: "projects.nav.compare" },
  { href: "reports", labelKey: "projects.nav.reports" },
  { href: "assumptions", labelKey: "projects.nav.assumptions" },
  { href: "history", labelKey: "projects.nav.history" },
];

export function ProjectSectionNav({ projectId }: { projectId: string }) {
  const pathname = usePathname();
  const { t } = useI18n();

  return (
    <nav
      aria-label={t("projects.nav.label")}
      style={{
        border: "1px solid #e5e7eb",
        borderRadius: 8,
        background: "#fff",
        padding: 8,
        display: "flex",
        gap: 8,
        flexWrap: "wrap",
      }}
    >
      {sections.map((section) => {
        const href = section.href ? `/projects/${projectId}/${section.href}` : `/projects/${projectId}`;
        const active = pathname === href;

        return (
          <Link
            key={section.labelKey}
            href={href}
            style={{
              borderRadius: 8,
              padding: "8px 10px",
              background: active ? "#14365d" : "transparent",
              color: active ? "#fff" : "#142033",
              fontSize: 14,
              fontWeight: active ? 800 : 600,
            }}
          >
            {t(section.labelKey)}
          </Link>
        );
      })}
    </nav>
  );
}
