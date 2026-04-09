"use client";

import type { BacsDomain, BacsFunctionResponse } from "@/types/bacs";

const domainLabels: Record<BacsDomain, string> = {
  monitoring: "Monitoring",
  heating: "Heating",
  cooling_ventilation: "Cooling & ventilation",
  dhw: "DHW",
  lighting: "Lighting",
};

type BacsDomainSectionProps = {
  domain: BacsDomain;
  functions: BacsFunctionResponse[];
  selectedFunctionIds: string[];
  onToggle: (functionId: string, nextSelected: boolean) => void;
};

export function BacsDomainSection({ domain, functions, selectedFunctionIds, onToggle }: BacsDomainSectionProps) {
  return (
    <details open style={{ border: "1px solid #e5e7eb", borderRadius: 16, padding: 18, background: "#fff" }}>
      <summary style={{ cursor: "pointer", listStyle: "none" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
          <div style={{ fontSize: 18, fontWeight: 700 }}>{domainLabels[domain]}</div>
          <div style={{ color: "#627084", fontSize: 14 }}>{functions.length} question(s)</div>
        </div>
      </summary>

      <div style={{ display: "grid", gap: 12, marginTop: 16 }}>
        {functions.map((item) => {
          const isSelected = selectedFunctionIds.includes(item.id);

          return (
            <div key={item.id} style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 16, display: "grid", gap: 10 }}>
              <div style={{ display: "grid", gap: 4 }}>
                <div style={{ fontSize: 15, fontWeight: 700 }}>{item.name}</div>
                <div style={{ fontSize: 13, color: "#627084" }}>
                  {item.description ?? "Description indisponible."}
                </div>
              </div>

              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
                <div style={{ fontSize: 13, color: "#475569" }}>Poids {item.weight}</div>
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
                    Oui
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
                    Non
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
