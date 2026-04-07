"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { ApiError } from "@/lib/api-client/errors";
import { useBuilding } from "../hooks/use-building";
import type { BuildingPayload, Orientation } from "@/types/building";

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

type BuildingStepFormValues = {
  name: string;
  construction_period: string;
  gross_floor_area_m2: string;
  heated_area_m2: string;
  cooled_area_m2: string;
  number_of_floors: string;
  number_of_rooms: string;
  main_orientation: "" | Orientation;
  compactness_level: string;
  has_restaurant: boolean;
  has_meeting_rooms: boolean;
  has_spa: boolean;
  has_pool: boolean;
};

function toNullableString(value: string) {
  const normalized = value.trim();
  return normalized.length > 0 ? normalized : null;
}

function toNullableNumber(value: string) {
  const normalized = value.trim();
  return normalized.length > 0 ? Number(normalized) : null;
}

function toFormValues(payload?: Partial<BuildingPayload> | null): BuildingStepFormValues {
  return {
    name: payload?.name ?? "",
    construction_period: payload?.construction_period ?? "",
    gross_floor_area_m2: payload?.gross_floor_area_m2?.toString() ?? "",
    heated_area_m2: payload?.heated_area_m2?.toString() ?? "",
    cooled_area_m2: payload?.cooled_area_m2?.toString() ?? "",
    number_of_floors: payload?.number_of_floors?.toString() ?? "",
    number_of_rooms: payload?.number_of_rooms?.toString() ?? "",
    main_orientation: payload?.main_orientation ?? "",
    compactness_level: payload?.compactness_level ?? "",
    has_restaurant: payload?.has_restaurant ?? false,
    has_meeting_rooms: payload?.has_meeting_rooms ?? false,
    has_spa: payload?.has_spa ?? false,
    has_pool: payload?.has_pool ?? false,
  };
}

function toPayload(values: BuildingStepFormValues): BuildingPayload {
  return {
    name: toNullableString(values.name),
    construction_period: toNullableString(values.construction_period),
    gross_floor_area_m2: toNullableNumber(values.gross_floor_area_m2),
    heated_area_m2: toNullableNumber(values.heated_area_m2),
    cooled_area_m2: toNullableNumber(values.cooled_area_m2),
    number_of_floors: toNullableNumber(values.number_of_floors),
    number_of_rooms: toNullableNumber(values.number_of_rooms),
    main_orientation: values.main_orientation || null,
    compactness_level: toNullableString(values.compactness_level),
    has_restaurant: values.has_restaurant,
    has_meeting_rooms: values.has_meeting_rooms,
    has_spa: values.has_spa,
    has_pool: values.has_pool,
  };
}

type BuildingStepFormProps = {
  projectId: string;
  onSaved?: () => Promise<unknown> | unknown;
};

export function BuildingStepForm({ projectId, onSaved }: BuildingStepFormProps) {
  const { data, isLoading, saveBuilding } = useBuilding(projectId);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const { register, handleSubmit, reset } = useForm<BuildingStepFormValues>({
    defaultValues: toFormValues(null),
  });

  useEffect(() => {
    reset(toFormValues(data?.data));
  }, [data, reset]);

  const onSubmit = async (values: BuildingStepFormValues) => {
    setSubmitError(null);

    try {
      await saveBuilding.mutateAsync(toPayload(values));
      await onSaved?.();
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : "Enregistrement du batiment impossible.");
    }
  };

  if (isLoading) {
    return <div>Chargement du batiment...</div>;
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ display: "grid", gap: 20 }}>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <div style={{ display: "grid", gap: 6 }}>
          <label htmlFor="building_name" style={{ fontSize: 14, fontWeight: 600 }}>Nom du batiment</label>
          <input id="building_name" {...register("name")} style={inputStyle} />
        </div>
        <div style={{ display: "grid", gap: 6 }}>
          <label htmlFor="construction_period" style={{ fontSize: 14, fontWeight: 600 }}>Periode de construction</label>
          <input id="construction_period" {...register("construction_period")} style={inputStyle} />
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 16 }}>
        <div style={{ display: "grid", gap: 6 }}>
          <label htmlFor="gross_floor_area_m2" style={{ fontSize: 14, fontWeight: 600 }}>Surface brute (m2)</label>
          <input id="gross_floor_area_m2" type="number" step="0.1" {...register("gross_floor_area_m2")} style={inputStyle} />
        </div>
        <div style={{ display: "grid", gap: 6 }}>
          <label htmlFor="heated_area_m2" style={{ fontSize: 14, fontWeight: 600 }}>Surface chauffee (m2)</label>
          <input id="heated_area_m2" type="number" step="0.1" {...register("heated_area_m2")} style={inputStyle} />
        </div>
        <div style={{ display: "grid", gap: 6 }}>
          <label htmlFor="cooled_area_m2" style={{ fontSize: 14, fontWeight: 600 }}>Surface refroidie (m2)</label>
          <input id="cooled_area_m2" type="number" step="0.1" {...register("cooled_area_m2")} style={inputStyle} />
        </div>
        <div style={{ display: "grid", gap: 6 }}>
          <label htmlFor="compactness_level" style={{ fontSize: 14, fontWeight: 600 }}>Niveau de compacite</label>
          <input id="compactness_level" {...register("compactness_level")} style={inputStyle} />
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 16 }}>
        <div style={{ display: "grid", gap: 6 }}>
          <label htmlFor="number_of_floors" style={{ fontSize: 14, fontWeight: 600 }}>Nombre d'etages</label>
          <input id="number_of_floors" type="number" step="1" {...register("number_of_floors")} style={inputStyle} />
        </div>
        <div style={{ display: "grid", gap: 6 }}>
          <label htmlFor="number_of_rooms" style={{ fontSize: 14, fontWeight: 600 }}>Nombre de chambres</label>
          <input id="number_of_rooms" type="number" step="1" {...register("number_of_rooms")} style={inputStyle} />
        </div>
        <div style={{ display: "grid", gap: 6 }}>
          <label htmlFor="main_orientation" style={{ fontSize: 14, fontWeight: 600 }}>Orientation principale</label>
          <select id="main_orientation" {...register("main_orientation")} style={inputStyle}>
            <option value="">Selectionner</option>
            {orientationOptions.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 12 }}>
        {[
          ["has_restaurant", "Restaurant"],
          ["has_meeting_rooms", "Salles de reunion"],
          ["has_spa", "Spa"],
          ["has_pool", "Piscine"],
        ].map(([field, label]) => (
          <label key={field} style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 14 }}>
            <input type="checkbox" {...register(field as keyof BuildingStepFormValues)} />
            {label}
          </label>
        ))}
      </div>

      {submitError ? (
        <div style={{ border: "1px solid #fecaca", borderRadius: 12, background: "#fff", padding: 16, color: "#b91c1c" }}>
          {submitError}
        </div>
      ) : null}

      <div style={{ display: "flex", justifyContent: "flex-end" }}>
        <button
          type="submit"
          disabled={saveBuilding.isPending}
          style={{
            borderRadius: 10,
            border: "1px solid #14365d",
            background: "#14365d",
            color: "#fff",
            padding: "10px 14px",
            fontWeight: 600,
            cursor: saveBuilding.isPending ? "not-allowed" : "pointer",
          }}
        >
          {saveBuilding.isPending ? "Enregistrement..." : "Enregistrer le batiment"}
        </button>
      </div>
    </form>
  );
}
