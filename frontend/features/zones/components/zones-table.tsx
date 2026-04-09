"use client";

import type { BuildingZoneResponse } from "@/types/zones";

type ZonesTableProps = {
  zones: BuildingZoneResponse[];
  deletingZoneId?: string | null;
  onAdd: () => void;
  onEdit: (zone: BuildingZoneResponse) => void;
  onDelete: (zone: BuildingZoneResponse) => Promise<void> | void;
};

export function ZonesTable({ zones, deletingZoneId, onAdd, onEdit, onDelete }: ZonesTableProps) {
  return (
    <section style={{ border: "1px solid #e5e7eb", borderRadius: 16, overflow: "hidden" }}>
      <div
        style={{
          padding: 20,
          borderBottom: "1px solid #e5e7eb",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: 12,
        }}
      >
        <div style={{ display: "grid", gap: 4 }}>
          <div style={{ fontSize: 18, fontWeight: 700 }}>Zones definies</div>
          <div style={{ color: "#627084", fontSize: 14 }}>
            Editez les zones existantes ou ajoutez des zones complementaires.
          </div>
        </div>
        <button
          type="button"
          onClick={onAdd}
          style={{ borderRadius: 10, border: "1px solid #14365d", background: "#fff", color: "#14365d", padding: "10px 14px", fontWeight: 700 }}
        >
          Ajouter une zone
        </button>
      </div>

      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#f8fafc", color: "#334155", textAlign: "left" }}>
              {["Ordre", "Nom", "Type", "Orientation", "Surface (m2)", "Chambres", "Actions"].map((label) => (
                <th key={label} style={{ padding: "14px 16px", fontSize: 13, fontWeight: 700, borderBottom: "1px solid #e5e7eb" }}>
                  {label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {zones.map((zone) => (
              <tr key={zone.id}>
                <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>{zone.order_index}</td>
                <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14, fontWeight: 600 }}>{zone.name}</td>
                <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>{zone.zone_type}</td>
                <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>{zone.orientation}</td>
                <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>{zone.area_m2}</td>
                <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>{zone.room_count}</td>
                <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 14 }}>
                  <div style={{ display: "flex", gap: 10 }}>
                    <button
                      type="button"
                      onClick={() => onEdit(zone)}
                      style={{ border: "1px solid #cbd5e1", background: "#fff", borderRadius: 8, padding: "8px 12px" }}
                    >
                      Editer
                    </button>
                    <button
                      type="button"
                      onClick={() => onDelete(zone)}
                      disabled={deletingZoneId === zone.id}
                      style={{ border: "1px solid #fecaca", background: "#fff", color: "#b91c1c", borderRadius: 8, padding: "8px 12px" }}
                    >
                      {deletingZoneId === zone.id ? "Suppression..." : "Supprimer"}
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
