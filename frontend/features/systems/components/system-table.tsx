"use client";

import type { SystemType, TechnicalSystemResponse } from "@/types/systems";
import {
  efficiencyLevelOptions,
  energySourceOptions,
  systemTypeOptions,
  technologyTypeOptions,
} from "./system-editor-dialog";

const systemTypeLabels = Object.fromEntries(systemTypeOptions.map((option) => [option.value, option.label])) as Record<SystemType, string>;
const energySourceLabels = Object.fromEntries(energySourceOptions.map((option) => [option.value, option.label])) as Record<string, string>;
const technologyTypeLabels = Object.fromEntries(technologyTypeOptions.map((option) => [option.value, option.label])) as Record<string, string>;
const efficiencyLevelLabels = Object.fromEntries(efficiencyLevelOptions.map((option) => [option.value, option.label])) as Record<string, string>;

type SystemTableProps = {
  systemsByType: Array<{ systemType: SystemType; items: TechnicalSystemResponse[] }>;
  deletingSystemId?: string | null;
  onAdd: (systemType?: SystemType) => void;
  onEdit: (system: TechnicalSystemResponse) => void;
  onDelete: (system: TechnicalSystemResponse) => Promise<void> | void;
};

export function SystemTable({ systemsByType, deletingSystemId, onAdd, onEdit, onDelete }: SystemTableProps) {
  return (
    <div style={{ display: "grid", gap: 16 }}>
      {systemsByType.map((group) => (
        <section key={group.systemType} style={{ border: "1px solid #e5e7eb", borderRadius: 16, overflow: "hidden" }}>
          <div
            style={{
              padding: 20,
              borderBottom: "1px solid #e5e7eb",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              gap: 12,
              background: "#f8fafc",
            }}
          >
            <div style={{ display: "grid", gap: 4 }}>
              <div style={{ fontSize: 18, fontWeight: 700 }}>{systemTypeLabels[group.systemType]}</div>
              <div style={{ color: "#627084", fontSize: 14 }}>{group.items.length} systeme(s) enregistre(s)</div>
            </div>
            <button
              type="button"
              onClick={() => onAdd(group.systemType)}
              style={{ borderRadius: 10, border: "1px solid #14365d", background: "#fff", color: "#14365d", padding: "10px 14px", fontWeight: 700 }}
            >
              Ajouter
            </button>
          </div>

          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ textAlign: "left", color: "#334155" }}>
                  {["Ordre", "Nom", "Energie", "Technologie", "Efficacite", "Principal", "Quantite", "Annee", "Dessert", "Actions"].map((label) => (
                    <th key={label} style={{ padding: "14px 16px", fontSize: 13, fontWeight: 700, borderBottom: "1px solid #e5e7eb" }}>
                      {label}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {group.items.map((system) => (
                  <tr key={system.id}>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>{system.order_index}</td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14, fontWeight: 600 }}>
                      <div style={{ display: "grid", gap: 4 }}>
                        <div>{system.name}</div>
                        {system.notes ? <div style={{ color: "#627084", fontWeight: 400 }}>{system.notes}</div> : null}
                      </div>
                    </td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>
                      {system.energy_source ? energySourceLabels[system.energy_source] ?? system.energy_source : "Non renseigne"}
                    </td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>
                      {system.technology_type ? technologyTypeLabels[system.technology_type] ?? system.technology_type : "Non renseigne"}
                    </td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>
                      {system.efficiency_level ? efficiencyLevelLabels[system.efficiency_level] ?? system.efficiency_level : "Non renseigne"}
                    </td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>{system.is_primary ? "Oui" : "Non"}</td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>{system.quantity ?? "-"}</td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>{system.year_installed ?? "-"}</td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>{system.serves ?? "-"}</td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>
                      <div style={{ display: "flex", gap: 10 }}>
                        <button
                          type="button"
                          onClick={() => onEdit(system)}
                          style={{ border: "1px solid #cbd5e1", background: "#fff", borderRadius: 8, padding: "8px 12px" }}
                        >
                          Editer
                        </button>
                        <button
                          type="button"
                          onClick={() => onDelete(system)}
                          disabled={deletingSystemId === system.id}
                          style={{ border: "1px solid #fecaca", background: "#fff", color: "#b91c1c", borderRadius: 8, padding: "8px 12px" }}
                        >
                          {deletingSystemId === system.id ? "Suppression..." : "Supprimer"}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      ))}
    </div>
  );
}
