"use client";

import Link from "next/link";
import { AdminGuard } from "./admin-guard";
import { useI18n } from "@/providers/i18n-provider";

const cards = [
  { href: "/admin/users", titleKey: "admin.users.title", bodyKey: "admin.users.description" },
  { href: "/admin/branding", titleKey: "admin.branding.title", bodyKey: "admin.branding.description" },
  { href: "/admin", titleKey: "admin.references.title", bodyKey: "admin.references.description", disabled: true },
];

export function AdminLandingPage() {
  const { t } = useI18n();

  return (
    <AdminGuard>
      <div style={{ display: "grid", gap: 20 }}>
        <div style={{ display: "grid", gap: 6 }}>
          <div style={{ fontSize: 13, color: "#627084", textTransform: "uppercase", letterSpacing: 0 }}>{t("admin.eyebrow")}</div>
          <h1 style={{ margin: 0, fontSize: 30, fontWeight: 800 }}>{t("admin.title")}</h1>
          <p style={{ margin: 0, color: "#627084", maxWidth: 760 }}>{t("admin.description")}</p>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: 16 }}>
          {cards.map((card) => (
            <Link
              key={card.titleKey}
              href={card.href}
              aria-disabled={card.disabled}
              style={{
                border: "1px solid #e5e7eb",
                borderRadius: 8,
                background: "#fff",
                padding: 20,
                display: "grid",
                gap: 8,
                opacity: card.disabled ? 0.65 : 1,
                pointerEvents: card.disabled ? "none" : "auto",
              }}
            >
              <div style={{ fontSize: 18, fontWeight: 800 }}>{t(card.titleKey)}</div>
              <div style={{ color: "#627084", fontSize: 14 }}>{t(card.bodyKey)}</div>
              {card.disabled ? <div style={{ color: "#92400e", fontSize: 13 }}>{t("admin.references.stub")}</div> : null}
            </Link>
          ))}
        </div>
      </div>
    </AdminGuard>
  );
}
