import { env } from "@/lib/config/env";
import type { BrandingProfile } from "@/types/branding";
import { getBrandingAccentColor, getBrandingInitials } from "../utils/branding";

type BrandMarkProps = {
  profile?: BrandingProfile | null;
  size?: "sm" | "md";
  showName?: boolean;
};

export function BrandMark({ profile, size = "md", showName = true }: BrandMarkProps) {
  const accentColor = getBrandingAccentColor(profile);
  const label = profile?.company_name ?? env.appName;
  const logoText = profile?.logo_text ?? (getBrandingInitials(label) || "HEA");
  const markSize = size === "sm" ? 32 : 40;

  return (
    <div style={{ display: "inline-flex", alignItems: "center", gap: 10, minWidth: 0 }}>
      <div
        aria-label={label}
        style={{
          width: markSize,
          height: markSize,
          borderRadius: 8,
          border: `2px solid ${accentColor}`,
          background: "#fff",
          color: "#142033",
          display: "grid",
          placeItems: "center",
          fontSize: size === "sm" ? 12 : 14,
          fontWeight: 800,
          flex: "0 0 auto",
        }}
      >
        {logoText}
      </div>
      {showName ? (
        <div style={{ display: "grid", minWidth: 0 }}>
          <span style={{ color: "#142033", fontWeight: 700, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            {label}
          </span>
          {profile ? (
            <span style={{ color: "#627084", fontSize: 12, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
              {profile.name}
            </span>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
