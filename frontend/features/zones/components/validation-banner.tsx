"use client";

import type { ZoneValidationItem } from "@/types/zones";

const statusColors: Record<ZoneValidationItem["status"], { border: string; background: string; color: string }> = {
  ok: { border: "#bbf7d0", background: "#f0fdf4", color: "#166534" },
  warning: { border: "#fde68a", background: "#fffbeb", color: "#92400e" },
  error: { border: "#fecaca", background: "#fef2f2", color: "#b91c1c" },
};

type ValidationBannerProps = {
  isValid: boolean;
  checks: ZoneValidationItem[];
  warnings: ZoneValidationItem[];
};

export function ValidationBanner({ isValid, checks, warnings }: ValidationBannerProps) {
  const errorChecks = checks.filter((item) => item.status === "error");
  const okChecks = checks.filter((item) => item.status === "ok");
  const summaryStyle = isValid ? statusColors.ok : statusColors.error;

  return (
    <section
      style={{
        border: `1px solid ${summaryStyle.border}`,
        background: summaryStyle.background,
        borderRadius: 16,
        padding: 16,
        display: "grid",
        gap: 12,
      }}
    >
      <div style={{ display: "grid", gap: 4 }}>
        <div style={{ fontSize: 14, fontWeight: 700, color: summaryStyle.color }}>
          {isValid ? "Validation zones OK" : "Validation zones a corriger"}
        </div>
        <div style={{ fontSize: 14, color: "#334155" }}>
          {isValid
            ? "Les controles bloquants sont passes. Vous pouvez continuer en gardant un oeil sur les avertissements."
            : "Certaines incoherences bloquantes doivent etre resolues avant de poursuivre."}
        </div>
      </div>

      {errorChecks.length > 0 ? (
        <div style={{ display: "grid", gap: 8 }}>
          {errorChecks.map((item) => (
            <div key={item.code} style={{ color: statusColors.error.color, fontSize: 14 }}>
              {item.message}
            </div>
          ))}
        </div>
      ) : null}

      {warnings.length > 0 ? (
        <div style={{ display: "grid", gap: 8 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: statusColors.warning.color }}>
            Avertissements
          </div>
          {warnings.map((item) => (
            <div key={item.code} style={{ color: statusColors.warning.color, fontSize: 14 }}>
              {item.message}
            </div>
          ))}
        </div>
      ) : null}

      {okChecks.length > 0 ? (
        <div style={{ display: "grid", gap: 8 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: statusColors.ok.color }}>
            Controles passes
          </div>
          {okChecks.map((item) => (
            <div key={item.code} style={{ color: statusColors.ok.color, fontSize: 14 }}>
              {item.message}
            </div>
          ))}
        </div>
      ) : null}
    </section>
  );
}
