"use client";

import { useEffect } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import type { EnergySource, SystemType, TechnicalSystemResponse } from "@/types/systems";
import { systemEditorSchema, type SystemEditorFormValues } from "../schemas/system-schema";

const inputStyle = {
  width: "100%",
  borderRadius: 8,
  border: "1px solid #d1d5db",
  padding: "10px 12px",
  fontSize: 14,
  background: "#fff",
} as const;

export const systemTypeOptions: Array<{ value: SystemType; label: string }> = [
  { value: "heating", label: "Heating" },
  { value: "cooling", label: "Cooling" },
  { value: "ventilation", label: "Ventilation" },
  { value: "dhw", label: "DHW" },
  { value: "lighting", label: "Lighting" },
  { value: "auxiliaries", label: "Auxiliaries" },
  { value: "control", label: "Control" },
];

export const energySourceOptions: Array<{ value: EnergySource; label: string }> = [
  { value: "electricity", label: "Electricity" },
  { value: "natural_gas", label: "Natural gas" },
  { value: "fuel_oil", label: "Fuel oil" },
  { value: "district_heating", label: "District heating" },
  { value: "district_cooling", label: "District cooling" },
  { value: "lpg", label: "LPG" },
  { value: "biomass", label: "Biomass" },
  { value: "solar", label: "Solar" },
  { value: "ambient", label: "Ambient" },
  { value: "other", label: "Other" },
];

function toFormValues(system?: Partial<TechnicalSystemResponse> | null): SystemEditorFormValues {
  return {
    name: system?.name ?? "",
    system_type: system?.system_type ?? "heating",
    energy_source: system?.energy_source ?? "",
    serves: system?.serves ?? "",
    quantity: system?.quantity?.toString() ?? "",
    year_installed: system?.year_installed?.toString() ?? "",
    is_primary: system?.is_primary ?? false,
    notes: system?.notes ?? "",
    order_index: system?.order_index?.toString() ?? "0",
  };
}

type SystemEditorDialogProps = {
  system?: TechnicalSystemResponse | null;
  initialSystemType?: SystemType;
  isOpen: boolean;
  isPending: boolean;
  onClose: () => void;
  onSubmit: (values: SystemEditorFormValues) => Promise<void> | void;
};

export function SystemEditorDialog({
  system,
  initialSystemType = "heating",
  isOpen,
  isPending,
  onClose,
  onSubmit,
}: SystemEditorDialogProps) {
  const initialValues = system ?? { system_type: initialSystemType };

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<SystemEditorFormValues>({
    resolver: zodResolver(systemEditorSchema),
    defaultValues: toFormValues(initialValues),
  });

  useEffect(() => {
    reset(toFormValues(system ?? { system_type: initialSystemType }));
  }, [initialSystemType, reset, system]);

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
      <div style={{ width: "min(760px, 100%)", background: "#fff", borderRadius: 20, padding: 24, display: "grid", gap: 16 }}>
        <div style={{ display: "grid", gap: 4 }}>
          <div style={{ fontSize: 20, fontWeight: 700 }}>{system ? "Editer un systeme" : "Ajouter un systeme"}</div>
          <div style={{ color: "#627084", fontSize: 14 }}>
            Renseignez les caracteristiques principales du systeme. Les details avances restent optionnels.
          </div>
        </div>

        <form onSubmit={handleSubmit(async (values) => onSubmit(values))} style={{ display: "grid", gap: 16 }}>
          <div style={{ display: "grid", gridTemplateColumns: "1.4fr 1fr 1fr", gap: 12 }}>
            <div style={{ display: "grid", gap: 6 }}>
              <label htmlFor="system_name" style={{ fontSize: 14, fontWeight: 600 }}>Nom / technologie</label>
              <input id="system_name" {...register("name")} style={inputStyle} />
              {errors.name ? <div style={{ color: "#b91c1c", fontSize: 13 }}>{errors.name.message}</div> : null}
            </div>

            <div style={{ display: "grid", gap: 6 }}>
              <label htmlFor="system_type" style={{ fontSize: 14, fontWeight: 600 }}>Type</label>
              <select id="system_type" {...register("system_type")} style={inputStyle}>
                {systemTypeOptions.map((option) => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </div>

            <div style={{ display: "grid", gap: 6 }}>
              <label htmlFor="system_energy_source" style={{ fontSize: 14, fontWeight: 600 }}>Energie</label>
              <select id="system_energy_source" {...register("energy_source")} style={inputStyle}>
                <option value="">Non renseigne</option>
                {energySourceOptions.map((option) => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </div>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            <div style={{ display: "grid", gap: 6 }}>
              <label htmlFor="system_order_index" style={{ fontSize: 14, fontWeight: 600 }}>Ordre</label>
              <input id="system_order_index" type="number" min="0" step="1" {...register("order_index")} style={inputStyle} />
              {errors.order_index ? <div style={{ color: "#b91c1c", fontSize: 13 }}>{errors.order_index.message}</div> : null}
            </div>

            <label style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 14, fontWeight: 600, paddingTop: 30 }}>
              <input type="checkbox" {...register("is_primary")} />
              Systeme principal
            </label>
          </div>

          <details style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 16 }}>
            <summary style={{ cursor: "pointer", fontWeight: 700 }}>Details avances</summary>
            <div style={{ display: "grid", gap: 16, marginTop: 16 }}>
              <div style={{ display: "grid", gap: 6 }}>
                <label htmlFor="system_serves" style={{ fontSize: 14, fontWeight: 600 }}>Dessert</label>
                <input id="system_serves" {...register("serves")} style={inputStyle} />
                {errors.serves ? <div style={{ color: "#b91c1c", fontSize: 13 }}>{errors.serves.message}</div> : null}
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                <div style={{ display: "grid", gap: 6 }}>
                  <label htmlFor="system_quantity" style={{ fontSize: 14, fontWeight: 600 }}>Quantite</label>
                  <input id="system_quantity" type="number" min="1" step="1" {...register("quantity")} style={inputStyle} />
                  {errors.quantity ? <div style={{ color: "#b91c1c", fontSize: 13 }}>{errors.quantity.message}</div> : null}
                </div>

                <div style={{ display: "grid", gap: 6 }}>
                  <label htmlFor="system_year_installed" style={{ fontSize: 14, fontWeight: 600 }}>Annee d&apos;installation</label>
                  <input id="system_year_installed" type="number" min="1900" step="1" {...register("year_installed")} style={inputStyle} />
                  {errors.year_installed ? <div style={{ color: "#b91c1c", fontSize: 13 }}>{errors.year_installed.message}</div> : null}
                </div>
              </div>

              <div style={{ display: "grid", gap: 6 }}>
                <label htmlFor="system_notes" style={{ fontSize: 14, fontWeight: 600 }}>Notes</label>
                <textarea id="system_notes" rows={4} {...register("notes")} style={{ ...inputStyle, resize: "vertical" }} />
              </div>
            </div>
          </details>

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
              {isPending ? "Enregistrement..." : system ? "Enregistrer les modifications" : "Creer le systeme"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
