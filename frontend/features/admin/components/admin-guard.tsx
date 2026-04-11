"use client";

import Link from "next/link";
import type { ReactNode } from "react";
import { useAuthContext } from "@/providers/auth-provider";
import { useI18n } from "@/providers/i18n-provider";

export function AdminGuard({ children }: { children: ReactNode }) {
  const { isReady, user } = useAuthContext();
  const { t } = useI18n();

  if (!isReady) {
    return <div>{t("admin.loading")}</div>;
  }

  if (user?.role !== "org_admin") {
    return (
      <div style={{ border: "1px solid #fecaca", borderRadius: 8, background: "#fff", padding: 24, display: "grid", gap: 12, color: "#b91c1c" }}>
        <div style={{ fontSize: 20, fontWeight: 800 }}>{t("admin.forbiddenTitle")}</div>
        <div>{t("admin.forbiddenBody")}</div>
        <Link href="/projects" style={{ color: "#14365d", fontWeight: 700 }}>
          {t("admin.backToProjects")}
        </Link>
      </div>
    );
  }

  return <>{children}</>;
}
