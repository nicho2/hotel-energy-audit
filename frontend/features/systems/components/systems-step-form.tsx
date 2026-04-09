"use client";

import { useMemo, useState } from "react";
import { ApiError } from "@/lib/api-client/errors";
import type { SystemType, TechnicalSystemCreatePayload, TechnicalSystemResponse } from "@/types/systems";
import { useSystems } from "../hooks/use-systems";
import type { SystemEditorFormValues } from "../schemas/system-schema";
import { SystemEditorDialog, systemTypeOptions } from "./system-editor-dialog";
import { SystemTable } from "./system-table";

function toNullableString(value: string) {
  const normalized = value.trim();
  return normalized.length > 0 ? normalized : null;
}

function toNullableInteger(value: string) {
  const normalized = value.trim();
  return normalized.length > 0 ? Number(normalized) : null;
}

function toPayload(values: SystemEditorFormValues): TechnicalSystemCreatePayload {
  return {
    name: values.name.trim(),
    system_type: values.system_type,
    energy_source: values.energy_source || null,
    serves: toNullableString(values.serves),
    quantity: toNullableInteger(values.quantity),
    year_installed: toNullableInteger(values.year_installed),
    is_primary: values.is_primary,
    notes: toNullableString(values.notes),
    order_index: Number(values.order_index),
  };
}

type SystemsStepFormProps = {
  projectId: string;
  onSaved?: () => Promise<unknown> | unknown;
};

export function SystemsStepForm({ projectId, onSaved }: SystemsStepFormProps) {
  const systems = useSystems(projectId);
  const [editorSystem, setEditorSystem] = useState<TechnicalSystemResponse | null>(null);
  const [editorDefaultType, setEditorDefaultType] = useState<SystemType>("heating");
  const [isEditorOpen, setIsEditorOpen] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const groupedSystems = useMemo(() => {
    const items = systems.data?.data ?? [];

    return systemTypeOptions
      .map((option) => ({
        systemType: option.value,
        items: items.filter((item) => item.system_type === option.value),
      }))
      .filter((group) => group.items.length > 0);
  }, [systems.data?.data]);

  const openCreateDialog = (systemType: SystemType = "heating") => {
    setSubmitError(null);
    setEditorSystem(null);
    setEditorDefaultType(systemType);
    setIsEditorOpen(true);
  };

  const openEditDialog = (system: TechnicalSystemResponse) => {
    setSubmitError(null);
    setEditorSystem(system);
    setEditorDefaultType(system.system_type);
    setIsEditorOpen(true);
  };

  const closeDialog = () => {
    if (systems.createSystem.isPending || systems.updateSystem.isPending) {
      return;
    }

    setIsEditorOpen(false);
    setEditorSystem(null);
  };

  const handleSubmit = async (values: SystemEditorFormValues) => {
    setSubmitError(null);

    try {
      const payload = toPayload(values);

      if (editorSystem) {
        await systems.updateSystem.mutateAsync({ systemId: editorSystem.id, payload });
      } else {
        await systems.createSystem.mutateAsync({
          ...payload,
          system_type: payload.system_type || editorDefaultType,
        });
      }

      setIsEditorOpen(false);
      setEditorSystem(null);
      await onSaved?.();
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : "Enregistrement du systeme impossible.");
    }
  };

  const handleDelete = async (system: TechnicalSystemResponse) => {
    setSubmitError(null);

    const confirmed = window.confirm(`Supprimer le systeme "${system.name}" ?`);
    if (!confirmed) {
      return;
    }

    try {
      await systems.deleteSystem.mutateAsync(system.id);
      await onSaved?.();
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : "Suppression du systeme impossible.");
    }
  };

  const handleRefresh = async () => {
    setSubmitError(null);
    await Promise.all([systems.refetch(), onSaved?.()]);
  };

  if (systems.isLoading) {
    return <div>Chargement des systemes...</div>;
  }

  if (systems.error) {
    return (
      <div style={{ display: "grid", gap: 12 }}>
        <div style={{ border: "1px solid #fecaca", borderRadius: 12, background: "#fff", padding: 16, color: "#b91c1c" }}>
          Impossible de charger les systemes du projet.
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

  const allSystems = systems.data?.data ?? [];
  const isEditorPending = systems.createSystem.isPending || systems.updateSystem.isPending;
  const deletingSystemId = systems.deleteSystem.isPending ? systems.deleteSystem.variables ?? null : null;

  return (
    <div style={{ display: "grid", gap: 20 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
        <div style={{ display: "grid", gap: 4 }}>
          <div style={{ fontSize: 14, color: "#627084", textTransform: "uppercase", letterSpacing: "0.04em" }}>
            Systems
          </div>
          <div style={{ fontSize: 16, color: "#334155" }}>
            Decrivez les systemes principaux de chauffage, refroidissement, ventilation, ECS, eclairage et auxiliaires.
          </div>
        </div>
        <div style={{ display: "flex", gap: 10 }}>
          <button
            type="button"
            onClick={handleRefresh}
            disabled={systems.isFetching}
            style={{ borderRadius: 10, border: "1px solid #cbd5e1", background: "#fff", padding: "10px 14px", fontWeight: 600 }}
          >
            {systems.isFetching ? "Actualisation..." : "Rafraichir"}
          </button>
          <button
            type="button"
            onClick={() => openCreateDialog("heating")}
            style={{ borderRadius: 10, border: "1px solid #14365d", background: "#14365d", color: "#fff", padding: "10px 14px", fontWeight: 700 }}
          >
            Ajouter un systeme
          </button>
        </div>
      </div>

      {submitError ? (
        <div style={{ border: "1px solid #fecaca", borderRadius: 12, background: "#fff", padding: 16, color: "#b91c1c" }}>
          {submitError}
        </div>
      ) : null}

      {allSystems.length === 0 ? (
        <section style={{ border: "1px dashed #cbd5e1", borderRadius: 16, padding: 24, display: "grid", gap: 12, textAlign: "center" }}>
          <div style={{ fontSize: 18, fontWeight: 700 }}>Aucun systeme enregistre</div>
          <div style={{ color: "#627084" }}>
            Commencez par declarer les equipements principaux. Les details avances peuvent etre saisis plus tard.
          </div>
          <div style={{ display: "flex", justifyContent: "center" }}>
            <button
              type="button"
              onClick={() => openCreateDialog("heating")}
              style={{ borderRadius: 10, border: "1px solid #14365d", background: "#fff", color: "#14365d", padding: "10px 14px", fontWeight: 700 }}
            >
              Ajouter le premier systeme
            </button>
          </div>
        </section>
      ) : (
        <SystemTable
          systemsByType={groupedSystems}
          deletingSystemId={deletingSystemId}
          onAdd={openCreateDialog}
          onEdit={openEditDialog}
          onDelete={handleDelete}
        />
      )}

      <SystemEditorDialog
        system={editorSystem}
        initialSystemType={editorDefaultType}
        isOpen={isEditorOpen}
        isPending={isEditorPending}
        onClose={closeDialog}
        onSubmit={handleSubmit}
      />
    </div>
  );
}
