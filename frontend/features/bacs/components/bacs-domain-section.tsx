"use client";

import type { BacsDomain, BacsFunctionResponse } from "@/types/bacs";
import { useI18n } from "@/providers/i18n-provider";
import { getBacsFunctionDescription, getBacsFunctionName } from "../utils/bacs-i18n";

type BacsDomainSectionProps = {
  domain: BacsDomain;
  functions: BacsFunctionResponse[];
  selectedFunctionIds: string[];
  onToggle: (functionId: string, nextSelected: boolean) => void;
};

export function BacsDomainSection({ domain, functions, selectedFunctionIds, onToggle }: BacsDomainSectionProps) {
  const { t } = useI18n();

  return (
    <details open style={{ border: "1px solid #e5e7eb", borderRadius: 16, padding: 18, background: "#fff" }}>
      <summary style={{ cursor: "pointer", listStyle: "none" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
          <div style={{ fontSize: 18, fontWeight: 700 }}>{t(`wizard.bacs.domain.${domain}`)}</div>
          <div style={{ color: "#627084", fontSize: 14 }}>{t("wizard.bacs.questionCount", { count: functions.length })}</div>
        </div>
      </summary>

      <div style={{ display: "grid", gap: 12, marginTop: 16 }}>
        {functions.map((item) => {
          const isSelected = selectedFunctionIds.includes(item.id);

          return (
            <div key={item.id} style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 16, display: "grid", gap: 10 }}>
              <div style={{ display: "grid", gap: 4 }}>
                <div style={{ fontSize: 15, fontWeight: 700 }}>{getBacsFunctionName(item, t)}</div>
                <div style={{ fontSize: 13, color: "#627084" }}>
                  {getBacsFunctionDescription(item, t) ?? t("wizard.bacs.descriptionUnavailable")}
                </div>
              </div>

              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
                <div style={{ fontSize: 13, color: "#475569" }}>{t("wizard.bacs.weight", { weight: item.weight })}</div>
                <div style={{ display: "flex", gap: 8 }}>
                  <button
                    type="button"
                    onClick={() => onToggle(item.id, true)}
                    style={{
                      borderRadius: 999,
                      border: `1px solid ${isSelected ? "#166534" : "#cbd5e1"}`,
                      background: isSelected ? "#dcfce7" : "#fff",
                      color: isSelected ? "#166534" : "#334155",
                      padding: "8px 12px",
                      fontWeight: 700,
                    }}
                  >
                    {t("wizard.bacs.yes")}
                  </button>
                  <button
                    type="button"
                    onClick={() => onToggle(item.id, false)}
                    style={{
                      borderRadius: 999,
                      border: `1px solid ${!isSelected ? "#b91c1c" : "#cbd5e1"}`,
                      background: !isSelected ? "#fef2f2" : "#fff",
                      color: !isSelected ? "#b91c1c" : "#334155",
                      padding: "8px 12px",
                      fontWeight: 700,
                    }}
                  >
                    {t("wizard.bacs.no")}
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </details>
  );
}
