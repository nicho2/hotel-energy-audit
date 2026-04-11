"use client";

import { supportedLanguages, type Language } from "@/i18n";
import { useI18n } from "@/providers/i18n-provider";

export function LanguageSwitcher() {
  const { language, setLanguage, t } = useI18n();

  return (
    <label style={{ display: "inline-flex", alignItems: "center", gap: 8, fontSize: 13, color: "#627084" }}>
      <span>{t("language.label")}</span>
      <select
        aria-label={t("language.label")}
        value={language}
        onChange={(event) => setLanguage(event.target.value as Language)}
        style={{
          borderRadius: 8,
          border: "1px solid #d1d5db",
          background: "#fff",
          padding: "6px 8px",
          color: "#142033",
          fontWeight: 600,
        }}
      >
        {supportedLanguages.map((item) => (
          <option key={item} value={item}>
            {t(`language.${item}`)}
          </option>
        ))}
      </select>
    </label>
  );
}
