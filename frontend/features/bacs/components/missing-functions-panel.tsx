"use client";

import type { BacsMissingFunctionResponse } from "@/types/bacs";
import { useI18n } from "@/providers/i18n-provider";
import { getBacsFunctionDescription, getBacsFunctionName } from "../utils/bacs-i18n";

type MissingFunctionsPanelProps = {
  functions: BacsMissingFunctionResponse[];
};

export function MissingFunctionsPanel({ functions }: MissingFunctionsPanelProps) {
  const { t } = useI18n();

  return (
    <section style={{ border: "1px solid #e5e7eb", borderRadius: 16, padding: 20, display: "grid", gap: 14 }}>
      <div style={{ display: "grid", gap: 4 }}>
        <div style={{ fontSize: 18, fontWeight: 700 }}>{t("wizard.bacs.missingTitle")}</div>
        <div style={{ color: "#627084", fontSize: 14 }}>
          {t("wizard.bacs.missingDescription")}
        </div>
      </div>

      {functions.length === 0 ? (
        <div style={{ color: "#166534", background: "#f0fdf4", border: "1px solid #bbf7d0", borderRadius: 12, padding: 16 }}>
          {t("wizard.bacs.noMissingFunctions")}
        </div>
      ) : (
        <div style={{ display: "grid", gap: 10 }}>
          {functions.map((item) => (
            <div key={item.id} style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 16, display: "grid", gap: 6 }}>
              <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                <div style={{ fontWeight: 700 }}>{getBacsFunctionName(item, t)}</div>
                <div style={{ color: "#14365d", fontWeight: 700 }}>{t("wizard.bacs.weight", { weight: item.weight })}</div>
              </div>
              <div style={{ fontSize: 13, color: "#627084" }}>{t(`wizard.bacs.domain.${item.domain}`)}</div>
              <div style={{ fontSize: 14, color: "#334155" }}>{getBacsFunctionDescription(item, t) ?? t("wizard.bacs.descriptionUnavailable")}</div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
