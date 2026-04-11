"use client";

import type { BrandingProfile } from "@/types/branding";
import { useI18n } from "@/providers/i18n-provider";

type BrandingSelectProps = {
  id: string;
  value: string;
  profiles: BrandingProfile[];
  disabled?: boolean;
  onChange: (brandingProfileId: string) => void;
};

export function BrandingSelect({ id, value, profiles, disabled = false, onChange }: BrandingSelectProps) {
  const { t } = useI18n();

  return (
    <select
      id={id}
      value={value}
      disabled={disabled}
      onChange={(event) => onChange(event.target.value)}
      style={{
        width: "100%",
        borderRadius: 8,
        border: "1px solid #d1d5db",
        padding: "10px 12px",
        fontSize: 14,
        background: "#fff",
      }}
    >
      <option value="">{t("branding.defaultOption")}</option>
      {profiles.map((profile) => (
        <option key={profile.id} value={profile.id}>
          {profile.company_name}{profile.is_default ? ` (${t("branding.defaultBadge")})` : ""}
        </option>
      ))}
    </select>
  );
}
