"use client";

import type { BacsMissingFunctionResponse } from "@/types/bacs";

const domainLabels: Record<string, string> = {
  monitoring: "Monitoring",
  heating: "Heating",
  cooling_ventilation: "Cooling & ventilation",
  dhw: "DHW",
  lighting: "Lighting",
};

type MissingFunctionsPanelProps = {
  functions: BacsMissingFunctionResponse[];
};

export function MissingFunctionsPanel({ functions }: MissingFunctionsPanelProps) {
  return (
    <section style={{ border: "1px solid #e5e7eb", borderRadius: 16, padding: 20, display: "grid", gap: 14 }}>
      <div style={{ display: "grid", gap: 4 }}>
        <div style={{ fontSize: 18, fontWeight: 700 }}>Top missing functions</div>
        <div style={{ color: "#627084", fontSize: 14 }}>
          Les fonctions les plus impactantes non cochees apparaissent ici pour guider le commercial ou le pre-audit.
        </div>
      </div>

      {functions.length === 0 ? (
        <div style={{ color: "#166534", background: "#f0fdf4", border: "1px solid #bbf7d0", borderRadius: 12, padding: 16 }}>
          Aucune fonction a fort impact manquante dans le catalogue courant.
        </div>
      ) : (
        <div style={{ display: "grid", gap: 10 }}>
          {functions.map((item) => (
            <div key={item.id} style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 16, display: "grid", gap: 6 }}>
              <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                <div style={{ fontWeight: 700 }}>{item.name}</div>
                <div style={{ color: "#14365d", fontWeight: 700 }}>Poids {item.weight}</div>
              </div>
              <div style={{ fontSize: 13, color: "#627084" }}>{domainLabels[item.domain] ?? item.domain}</div>
              <div style={{ fontSize: 14, color: "#334155" }}>{item.description ?? "Description indisponible."}</div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
