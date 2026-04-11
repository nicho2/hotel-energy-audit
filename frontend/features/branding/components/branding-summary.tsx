import type { BrandingProfile } from "@/types/branding";
import { useI18n } from "@/providers/i18n-provider";
import { BrandMark } from "./brand-mark";

type BrandingSummaryProps = {
  profile?: BrandingProfile | null;
  isLoading?: boolean;
};

export function BrandingSummary({ profile, isLoading = false }: BrandingSummaryProps) {
  const { t } = useI18n();

  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 12, background: "#fff", padding: 14, display: "grid", gap: 10 }}>
      <div style={{ fontSize: 12, color: "#627084", textTransform: "uppercase", letterSpacing: "0.04em" }}>
        {t("branding.label")}
      </div>
      {isLoading ? (
        <div style={{ color: "#627084", fontSize: 14 }}>{t("branding.loading")}</div>
      ) : profile ? (
        <div style={{ display: "grid", gap: 8 }}>
          <BrandMark profile={profile} />
          <div style={{ color: "#627084", fontSize: 13 }}>
            {profile.contact_email ?? t("branding.noContact")}
          </div>
        </div>
      ) : (
        <div style={{ color: "#627084", fontSize: 14 }}>{t("branding.fallback")}</div>
      )}
    </div>
  );
}
