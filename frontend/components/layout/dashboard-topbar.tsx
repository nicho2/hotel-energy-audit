"use client";

import { env } from "@/lib/config/env";
import { LanguageSwitcher } from "@/components/i18n/language-switcher";
import { BrandMark } from "@/features/branding/components/brand-mark";
import { useBrandingProfiles } from "@/features/branding/hooks/use-branding-profiles";
import { getDefaultBrandingProfile, getBrandingAccentColor } from "@/features/branding/utils/branding";
import { useAuthContext } from "@/providers/auth-provider";
import { useI18n } from "@/providers/i18n-provider";

export function DashboardTopbar() {
  const { user } = useAuthContext();
  const { t } = useI18n();
  const brandingProfiles = useBrandingProfiles();
  const activeBranding = getDefaultBrandingProfile(brandingProfiles.data?.data ?? []);
  const accentColor = getBrandingAccentColor(activeBranding);

  return (
    <div
      style={{
        height: 64,
        borderBottom: "1px solid #e5e7eb",
        borderTop: `3px solid ${accentColor}`,
        background: "#fff",
        padding: "0 24px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <div style={{ display: "grid", gap: 2 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          {activeBranding ? <BrandMark profile={activeBranding} size="sm" showName={false} /> : null}
          <div style={{ fontWeight: 600 }}>{activeBranding?.company_name ?? env.appName}</div>
        </div>
        <div style={{ fontSize: 13, color: "#627084" }}>{t("app.workspace")}</div>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <LanguageSwitcher />
        <div style={{ fontSize: 14, color: "#627084" }}>
          {user ? user.email : t("app.unauthenticatedUser")}
        </div>
      </div>
    </div>
  );
}
