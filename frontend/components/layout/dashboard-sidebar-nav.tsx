"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { env } from "@/lib/config/env";
import { BrandMark } from "@/features/branding/components/brand-mark";
import { useBrandingProfiles } from "@/features/branding/hooks/use-branding-profiles";
import { getDefaultBrandingProfile } from "@/features/branding/utils/branding";
import { useAuthContext } from "@/providers/auth-provider";
import { useI18n } from "@/providers/i18n-provider";

const navItems = [
  { href: "/projects", labelKey: "nav.projects" },
  { href: "/templates", labelKey: "nav.templates" },
  { href: "/reports", labelKey: "nav.reports" },
  { href: "/catalog", labelKey: "nav.catalog" },
  { href: "/admin", labelKey: "nav.admin", adminOnly: true },
];

export function DashboardSidebarNav() {
  const pathname = usePathname();
  const { t } = useI18n();
  const { user } = useAuthContext();
  const brandingProfiles = useBrandingProfiles();
  const activeBranding = getDefaultBrandingProfile(brandingProfiles.data?.data ?? []);
  const visibleNavItems = navItems.filter((item) => !item.adminOnly || user?.role === "org_admin");

  return (
    <nav style={{ padding: 16, display: "grid", gap: 24 }}>
      <div style={{ display: "grid", gap: 4 }}>
        <div
          style={{
            fontSize: 12,
            fontWeight: 700,
            letterSpacing: 0,
            color: "#627084",
            textTransform: "uppercase",
          }}
        >
          MVP
        </div>
        {activeBranding ? (
          <BrandMark profile={activeBranding} />
        ) : (
          <div style={{ fontSize: 18, fontWeight: 700, color: "#142033" }}>{env.appName}</div>
        )}
      </div>

      <div style={{ display: "grid", gap: 8 }}>
        {visibleNavItems.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);

          return (
            <Link
              key={item.href}
              href={item.href}
              style={{
                display: "block",
                padding: "10px 12px",
                borderRadius: 8,
                background: isActive ? "#14365d" : "transparent",
                color: isActive ? "#ffffff" : "#142033",
                fontWeight: isActive ? 600 : 500,
              }}
            >
              {t(item.labelKey)}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
