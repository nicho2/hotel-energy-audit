"use client";

import { useEffect } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import type { Orientation } from "@/types/building";
import type { BuildingZoneResponse, ZoneType } from "@/types/zones";
import { zoneEditorSchema, type ZoneEditorFormValues } from "../schemas/zone-schema";

const inputStyle = {
  width: "100%",
  borderRadius: 8,
  border: "1px solid #d1d5db",
  padding: "10px 12px",
  fontSize: 14,
  background: "#fff",
} as const;

const orientationOptions: Array<{ value: Orientation; label: string }> = [
  { value: "north", label: "North" },
  { value: "south", label: "South" },
  { value: "east", label: "East" },
  { value: "west", label: "West" },
  { value: "mixed", label: "Mixed" },
];

const zoneTypeOptions: Array<{ value: ZoneType; label: string }> = [
  { value: "guest_rooms", label: "Guest rooms" },
  { value: "circulation", label: "Circulation" },
  { value: "lobby", label: "Lobby" },
  { value: "restaurant", label: "Restaurant" },
  { value: "meeting", label: "Meeting" },
  { value: "technical", label: "Technical" },
  { value: "spa", label: "Spa" },
  { value: "pool", label: "Pool" },
  { value: "other", label: "Other" },
];

function toFormValues(zone?: BuildingZoneResponse | null): ZoneEditorFormValues {
  return {
    name: zone?.name ?? "",
    zone_type: zone?.zone_type ?? "guest_rooms",
    orientation: zone?.orientation ?? "mixed",
    area_m2: zone?.area_m2?.toString() ?? "",
    room_count: zone?.room_count?.toString() ?? "0",
    order_index: zone?.order_index?.toString() ?? "0",
  };
}

type ZoneEditorDialogProps = {
  zone?: BuildingZoneResponse | null;
  isOpen: boolean;
  isPending: boolean;
  onClose: () => void;
  onSubmit: (values: ZoneEditorFormValues) => Promise<void> | void;
};

export function ZoneEditorDialog({ zone, isOpen, isPending, onClose, onSubmit }: ZoneEditorDialogProps) {
  const {
    register,
    watch,
    handleSubmit,
    reset,
    setValue,
    formState: { errors },
  } = useForm<ZoneEditorFormValues>({
    resolver: zodResolver(zoneEditorSchema),
    defaultValues: toFormValues(zone),
  });

  useEffect(() => {
    reset(toFormValues(zone));
  }, [zone, reset]);

  const zoneType = watch("zone_type");

  useEffect(() => {
    if (zoneType !== "guest_rooms") {
      setValue("room_count", "0", { shouldValidate: true });
    }
  }, [setValue, zoneType]);

  if (!isOpen) {
    return null;
  }

  return (
    <div
      role="dialog"
      aria-modal="true"
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(15, 23, 42, 0.45)",
        display: "grid",
        placeItems: "center",
        padding: 24,
        zIndex: 50,
      }}
    >
      <div style={{ width: "min(720px, 100%)", background: "#fff", borderRadius: 20, padding: 24, display: "grid", gap: 16 }}>
        <div style={{ display: "grid", gap: 4 }}>
          <div style={{ fontSize: 20, fontWeight: 700 }}>{zone ? "Editer une zone" : "Ajouter une zone"}</div>
          <div style={{ color: "#627084", fontSize: 14 }}>
            Modifiez les donnees de zone puis enregistrez pour persister via l&apos;API.
          </div>
        </div>

        <form onSubmit={handleSubmit(async (values) => onSubmit(values))} style={{ display: "grid", gap: 16 }}>
          <div style={{ display: "grid", gridTemplateColumns: "1.3fr 1fr 1fr", gap: 12 }}>
            <div style={{ display: "grid", gap: 6 }}>
              <label htmlFor="zone_name" style={{ fontSize: 14, fontWeight: 600 }}>Nom</label>
              <input id="zone_name" {...register("name")} style={inputStyle} />
              {errors.name ? <div style={{ color: "#b91c1c", fontSize: 13 }}>{errors.name.message}</div> : null}
            </div>

            <div style={{ display: "grid", gap: 6 }}>
              <label htmlFor="zone_type" style={{ fontSize: 14, fontWeight: 600 }}>Type</label>
              <select id="zone_type" {...register("zone_type")} style={inputStyle}>
                {zoneTypeOptions.map((option) => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </div>

            <div style={{ display: "grid", gap: 6 }}>
              <label htmlFor="zone_orientation" style={{ fontSize: 14, fontWeight: 600 }}>Orientation</label>
              <select id="zone_orientation" {...register("orientation")} style={inputStyle}>
                {orientationOptions.map((option) => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </div>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 12 }}>
            <div style={{ display: "grid", gap: 6 }}>
              <label htmlFor="zone_area_m2" style={{ fontSize: 14, fontWeight: 600 }}>Surface (m2)</label>
              <input id="zone_area_m2" type="number" min="0" step="0.1" {...register("area_m2")} style={inputStyle} />
              {errors.area_m2 ? <div style={{ color: "#b91c1c", fontSize: 13 }}>{errors.area_m2.message}</div> : null}
            </div>

            <div style={{ display: "grid", gap: 6 }}>
              <label htmlFor="zone_room_count" style={{ fontSize: 14, fontWeight: 600 }}>Nombre de chambres</label>
              <input
                id="zone_room_count"
                type="number"
                min="0"
                step="1"
                disabled={zoneType !== "guest_rooms"}
                {...register("room_count")}
                style={{ ...inputStyle, background: zoneType === "guest_rooms" ? "#fff" : "#f8fafc" }}
              />
              {errors.room_count ? <div style={{ color: "#b91c1c", fontSize: 13 }}>{errors.room_count.message}</div> : null}
            </div>

            <div style={{ display: "grid", gap: 6 }}>
              <label htmlFor="zone_order_index" style={{ fontSize: 14, fontWeight: 600 }}>Ordre</label>
              <input id="zone_order_index" type="number" min="0" step="1" {...register("order_index")} style={inputStyle} />
              {errors.order_index ? <div style={{ color: "#b91c1c", fontSize: 13 }}>{errors.order_index.message}</div> : null}
            </div>
          </div>

          <div style={{ display: "flex", justifyContent: "flex-end", gap: 12 }}>
            <button
              type="button"
              onClick={onClose}
              style={{ borderRadius: 10, border: "1px solid #cbd5e1", background: "#fff", padding: "10px 14px", fontWeight: 600 }}
            >
              Annuler
            </button>
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
              {isPending ? "Enregistrement..." : zone ? "Enregistrer les modifications" : "Creer la zone"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
