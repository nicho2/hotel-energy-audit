"use client";

import { LanguageSwitcher } from "@/components/i18n/language-switcher";
import { LoginForm } from "@/features/auth/components/login-form";
import { useI18n } from "@/providers/i18n-provider";

export default function LoginPage() {
  const { t } = useI18n();

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: 24 }}>
      <div style={{ width: "100%", maxWidth: 480, border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 32 }}>
        <div style={{ display: "flex", justifyContent: "space-between", gap: 16, alignItems: "center", marginBottom: 24 }}>
          <h1 style={{ fontSize: 28, fontWeight: 600, margin: 0 }}>{t("login.title")}</h1>
          <LanguageSwitcher />
        </div>
        <LoginForm />
      </div>
    </div>
  );
}
