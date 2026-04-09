"use client";

import { useMemo, useState } from "react";
import { ApiError } from "@/lib/api-client/errors";
import type { Orientation } from "@/types/building";
import type { BuildingZoneCreatePayload, BuildingZoneGeneratePayload, BuildingZoneResponse } from "@/types/zones";
import { useGenerateZones } from "../hooks/use-generate-zones";
import { useZoneValidation } from "../hooks/use-zone-validation";
import { useZones } from "../hooks/use-zones";
import type { ZoneEditorFormValues, ZoneGenerationFormValues } from "../schemas/zone-schema";
import { GenerationPanel } from "./generation-panel";
import { ValidationBanner } from "./validation-banner";
import { ZoneEditorDialog } from "./zone-editor-dialog";
import { ZonesTable } from "./zones-table";

function toNumber(value: string) {
  return Number(value.trim());
}

function toZonePayload(values: ZoneEditorFormValues): BuildingZoneCreatePayload {
  return {
    name: values.name.trim(),
    zone_type: values.zone_type,
    orientation: values.orientation,
    area_m2: toNumber(values.area_m2),
    room_count: values.zone_type === "guest_rooms" ? toNumber(values.room_count) : 0,
    order_index: toNumber(values.order_index),
  };
}

function toGeneratePayload(values: ZoneGenerationFormValues): BuildingZoneGeneratePayload {
  const distributions: Array<{ orientation: Orientation; room_count: number }> = [
    { orientation: "north", room_count: toNumber(values.north_rooms) },
    { orientation: "east", room_count: toNumber(values.east_rooms) },
    { orientation: "south", room_count: toNumber(values.south_rooms) },
    { orientation: "west", room_count: toNumber(values.west_rooms) },
    { orientation: "mixed", room_count: toNumber(values.mixed_rooms) },
  ];

  return {
    room_distribution: distributions.filter((item) => item.room_count > 0),
    average_room_area_m2: toNumber(values.average_room_area_m2),
    total_guest_room_area_m2: values.total_guest_room_area_m2.trim().length > 0 ? toNumber(values.total_guest_room_area_m2) : null,
    replace_existing: values.replace_existing,
  };
}

type ZonesStepFormProps = {
  projectId: string;
  onSaved?: () => Promise<unknown> | unknown;
};

export function ZonesStepForm({ projectId, onSaved }: ZonesStepFormProps) {
  const zones = useZones(projectId);
  const zoneValidation = useZoneValidation(projectId);
  const generateZones = useGenerateZones(projectId);

  const [editorZone, setEditorZone] = useState<BuildingZoneResponse | null>(null);
  const [isEditorOpen, setIsEditorOpen] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [generationWarnings, setGenerationWarnings] = useState<string[]>([]);

  const sortedZones = useMemo(
    () => [...(zones.data?.data ?? [])].sort((left, right) => left.order_index - right.order_index || left.name.localeCompare(right.name)),
    [zones.data?.data],
  );

  const openCreateDialog = () => {
    setSubmitError(null);
    setEditorZone(null);
    setIsEditorOpen(true);
  };

  const openEditDialog = (zone: BuildingZoneResponse) => {
    setSubmitError(null);
    setEditorZone(zone);
    setIsEditorOpen(true);
  };

  const closeDialog = () => {
    if (zones.createZone.isPending || zones.updateZone.isPending) {
      return;
    }

    setIsEditorOpen(false);
    setEditorZone(null);
  };

  const handleZoneSubmit = async (values: ZoneEditorFormValues) => {
    setSubmitError(null);

    try {
      const payload = toZonePayload(values);

      if (editorZone) {
        await zones.updateZone.mutateAsync({ zoneId: editorZone.id, payload });
      } else {
        await zones.createZone.mutateAsync(payload);
      }

      setIsEditorOpen(false);
      setEditorZone(null);
      await onSaved?.();
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : "Enregistrement de la zone impossible.");
    }
  };

  const handleDelete = async (zone: BuildingZoneResponse) => {
    setSubmitError(null);

    const confirmed = window.confirm(`Supprimer la zone "${zone.name}" ?`);
    if (!confirmed) {
      return;
    }

    try {
      await zones.deleteZone.mutateAsync(zone.id);
      await onSaved?.();
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : "Suppression de la zone impossible.");
    }
  };

  const handleGenerate = async (values: ZoneGenerationFormValues) => {
    setSubmitError(null);
    setGenerationWarnings([]);

    try {
      const response = await generateZones.mutateAsync(toGeneratePayload(values));
      setGenerationWarnings(Array.isArray(response.meta?.warnings) ? (response.meta.warnings as string[]) : []);
      await onSaved?.();
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : "Generation des zones impossible.");
    }
  };

  const handleRefresh = async () => {
    setSubmitError(null);
    await Promise.all([zones.refetch(), zoneValidation.refetch(), onSaved?.()]);
  };

  if (zones.isLoading || zoneValidation.isLoading) {
    return <div>Chargement des zones...</div>;
  }

  if (zones.error || zoneValidation.error) {
    return (
      <div style={{ display: "grid", gap: 12 }}>
        <div style={{ border: "1px solid #fecaca", borderRadius: 12, background: "#fff", padding: 16, color: "#b91c1c" }}>
          Impossible de charger les donnees de zonage.
        </div>
        <div>
          <button
            type="button"
            onClick={handleRefresh}
            style={{ borderRadius: 10, border: "1px solid #14365d", background: "#fff", color: "#14365d", padding: "10px 14px", fontWeight: 600 }}
          >
            Recharger
          </button>
        </div>
      </div>
    );
  }

  const validation = zoneValidation.data?.data;
  const hasZones = sortedZones.length > 0;
  const isEditorPending = zones.createZone.isPending || zones.updateZone.isPending;

  return (
    <div style={{ display: "grid", gap: 20 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
        <div style={{ display: "grid", gap: 4 }}>
          <div style={{ fontSize: 14, color: "#627084", textTransform: "uppercase", letterSpacing: "0.04em" }}>
            Zones
          </div>
          <div style={{ fontSize: 16, color: "#334155" }}>
            Generez, ajustez et validez le zonage fonctionnel du batiment.
          </div>
        </div>
        <button
          type="button"
          onClick={handleRefresh}
          disabled={zones.isFetching || zoneValidation.isFetching}
          style={{ borderRadius: 10, border: "1px solid #cbd5e1", background: "#fff", padding: "10px 14px", fontWeight: 600 }}
        >
          {zones.isFetching || zoneValidation.isFetching ? "Actualisation..." : "Rafraichir"}
        </button>
      </div>

      {validation ? <ValidationBanner isValid={validation.is_valid} checks={validation.checks} warnings={validation.warnings} /> : null}

      <GenerationPanel hasZones={hasZones} isPending={generateZones.isPending} onSubmit={handleGenerate} />

      {generationWarnings.length > 0 ? (
        <div style={{ border: "1px solid #fde68a", borderRadius: 12, background: "#fffbeb", padding: 16, color: "#92400e", display: "grid", gap: 8 }}>
          <div style={{ fontWeight: 700 }}>Avertissements de generation</div>
          {generationWarnings.map((warning) => (
            <div key={warning}>{warning}</div>
          ))}
        </div>
      ) : null}

      {submitError ? (
        <div style={{ border: "1px solid #fecaca", borderRadius: 12, background: "#fff", padding: 16, color: "#b91c1c" }}>
          {submitError}
        </div>
      ) : null}

      {!hasZones ? (
        <section style={{ border: "1px dashed #cbd5e1", borderRadius: 16, padding: 24, display: "grid", gap: 12, textAlign: "center" }}>
          <div style={{ fontSize: 18, fontWeight: 700 }}>Aucune zone enregistree</div>
          <div style={{ color: "#627084" }}>
            Generez une premiere proposition ou ajoutez une zone manuellement pour commencer.
          </div>
          <div style={{ display: "flex", justifyContent: "center" }}>
            <button
              type="button"
              onClick={openCreateDialog}
              style={{ borderRadius: 10, border: "1px solid #14365d", background: "#fff", color: "#14365d", padding: "10px 14px", fontWeight: 700 }}
            >
              Ajouter une premiere zone
            </button>
          </div>
        </section>
      ) : (
        <ZonesTable
          zones={sortedZones}
          deletingZoneId={zones.deleteZone.variables ?? null}
          onAdd={openCreateDialog}
          onEdit={openEditDialog}
          onDelete={handleDelete}
        />
      )}

      <ZoneEditorDialog
        zone={editorZone}
        isOpen={isEditorOpen}
        isPending={isEditorPending}
        onClose={closeDialog}
        onSubmit={handleZoneSubmit}
      />
    </div>
  );
}
