"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zoneGenerationSchema, type ZoneGenerationFormValues } from "../schemas/zone-schema";

const inputStyle = {
  width: "100%",
  borderRadius: 8,
  border: "1px solid #d1d5db",
  padding: "10px 12px",
  fontSize: 14,
  background: "#fff",
} as const;

type GenerationPanelProps = {
  hasZones: boolean;
  isPending: boolean;
  onSubmit: (values: ZoneGenerationFormValues) => Promise<void> | void;
};

export function GenerationPanel({ hasZones, isPending, onSubmit }: GenerationPanelProps) {
  const {
    register,
    handleSubmit,
    resetField,
    formState: { errors },
  } = useForm<ZoneGenerationFormValues>({
    resolver: zodResolver(zoneGenerationSchema),
    defaultValues: {
      north_rooms: "0",
      east_rooms: "0",
      south_rooms: "0",
      west_rooms: "0",
      mixed_rooms: "0",
      average_room_area_m2: "28",
      total_guest_room_area_m2: "",
      replace_existing: hasZones,
    },
  });

  useEffect(() => {
    resetField("replace_existing", { defaultValue: hasZones });
  }, [hasZones, resetField]);

  return (
    <section style={{ border: "1px solid #e5e7eb", borderRadius: 16, padding: 20, display: "grid", gap: 16 }}>
      <div style={{ display: "grid", gap: 4 }}>
        <div style={{ fontSize: 18, fontWeight: 700 }}>Generation de proposition</div>
        <div style={{ color: "#627084", fontSize: 14 }}>
          Repartissez les chambres par orientation pour generer une premiere base de zonage.
        </div>
      </div>

      <form onSubmit={handleSubmit(async (values) => onSubmit(values))} style={{ display: "grid", gap: 16 }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(5, minmax(0, 1fr))", gap: 12 }}>
          {[
            ["north_rooms", "Nord"],
            ["east_rooms", "Est"],
            ["south_rooms", "Sud"],
            ["west_rooms", "Ouest"],
            ["mixed_rooms", "Mixte"],
          ].map(([field, label]) => (
            <div key={field} style={{ display: "grid", gap: 6 }}>
              <label htmlFor={field} style={{ fontSize: 14, fontWeight: 600 }}>
                {label}
              </label>
              <input id={field} type="number" min="0" step="1" {...register(field as keyof ZoneGenerationFormValues)} style={inputStyle} />
            </div>
          ))}
        </div>

        {errors.north_rooms ? <div style={{ color: "#b91c1c", fontSize: 13 }}>{errors.north_rooms.message}</div> : null}

        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 12 }}>
          <div style={{ display: "grid", gap: 6 }}>
            <label htmlFor="average_room_area_m2" style={{ fontSize: 14, fontWeight: 600 }}>
              Surface moyenne par chambre (m2)
            </label>
            <input id="average_room_area_m2" type="number" min="0" step="0.1" {...register("average_room_area_m2")} style={inputStyle} />
            {errors.average_room_area_m2 ? <div style={{ color: "#b91c1c", fontSize: 13 }}>{errors.average_room_area_m2.message}</div> : null}
          </div>

          <div style={{ display: "grid", gap: 6 }}>
            <label htmlFor="total_guest_room_area_m2" style={{ fontSize: 14, fontWeight: 600 }}>
              Surface totale chambres (optionnel)
            </label>
            <input id="total_guest_room_area_m2" type="number" min="0" step="0.1" {...register("total_guest_room_area_m2")} style={inputStyle} />
            {errors.total_guest_room_area_m2 ? <div style={{ color: "#b91c1c", fontSize: 13 }}>{errors.total_guest_room_area_m2.message}</div> : null}
          </div>
        </div>

        <label style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 14 }}>
          <input type="checkbox" {...register("replace_existing")} />
          Remplacer les zones existantes pendant la generation
        </label>

        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <button
            type="submit"
            disabled={isPending}
            style={{
              borderRadius: 10,
              border: "1px solid #14365d",
              background: "#14365d",
              color: "#fff",
              padding: "10px 14px",
              fontWeight: 600,
              cursor: isPending ? "not-allowed" : "pointer",
            }}
          >
            {isPending ? "Generation..." : hasZones ? "Regenerer les zones" : "Generer une proposition"}
          </button>
        </div>
      </form>
    </section>
  );
}
