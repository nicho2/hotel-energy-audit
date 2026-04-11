import type { BrandingProfile } from "@/types/branding";

const fallbackAccentColor = "#14365d";

export function getBrandingAccentColor(profile?: BrandingProfile | null) {
  const value = profile?.accent_color?.trim();
  return value && /^#[0-9a-fA-F]{6}$/.test(value) ? value : fallbackAccentColor;
}

export function getDefaultBrandingProfile(profiles: BrandingProfile[]) {
  return profiles.find((profile) => profile.is_default) ?? profiles[0] ?? null;
}

export function getBrandingInitials(value: string) {
  return value
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join("");
}
