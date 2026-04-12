"use client";

import { useEffect, useMemo, useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { ApiError } from "@/lib/api-client/errors";
import { useAuthContext } from "@/providers/auth-provider";
import { FeedbackBlock, FieldError } from "@/components/ui/feedback";
import { saveStep } from "../api/save-step";
import { wizardDraftStepSchema, type WizardDraftStepValues } from "../schemas/wizard-draft-step-schema";

type FieldKind = "text" | "textarea" | "number" | "select" | "checkbox" | "csv";

type FieldDefinition = {
  name: string;
  label: string;
  kind: FieldKind;
  required?: boolean;
  helper?: string;
  options?: Array<{ value: string; label: string }>;
};

const inputStyle = {
  width: "100%",
  borderRadius: 8,
  border: "1px solid #d1d5db",
  padding: "10px 12px",
  fontSize: 14,
  background: "#fff",
} as const;

const stepFields: Record<string, FieldDefinition[]> = {
  project: [
    { name: "name", label: "Nom du projet", kind: "text", required: true },
    { name: "client_name", label: "Client", kind: "text" },
    { name: "reference_code", label: "Reference", kind: "text" },
    { name: "building_type", label: "Type de batiment", kind: "select", required: true, options: [
      { value: "hotel", label: "Hotel" },
      { value: "aparthotel", label: "Aparthotel" },
      { value: "residence", label: "Residence" },
      { value: "other_accommodation", label: "Autre hebergement" },
    ] },
    { name: "project_goal", label: "Objectif", kind: "text" },
    { name: "description", label: "Description", kind: "textarea" },
  ],
  context: [
    { name: "country_profile_id", label: "Profil pays", kind: "text", required: true, helper: "UUID du referentiel pays." },
    { name: "climate_zone_id", label: "Zone climatique", kind: "text", required: true, helper: "UUID du referentiel climat." },
    { name: "regulatory_frame", label: "Cadre de reference", kind: "text" },
    { name: "energy_price_electricity_eur_kwh", label: "Prix electricite EUR/kWh", kind: "number" },
    { name: "energy_price_gas_eur_kwh", label: "Prix gaz EUR/kWh", kind: "number" },
  ],
  usage: [
    { name: "average_occupancy_rate", label: "Taux d'occupation moyen", kind: "number", required: true, helper: "Valeur entre 0 et 1." },
    { name: "seasonality_profile", label: "Saisonnalite", kind: "select", options: [
      { value: "stable", label: "Stable" },
      { value: "seasonal", label: "Saisonnier" },
      { value: "highly_seasonal", label: "Tres saisonnier" },
    ] },
    { name: "room_usage_intensity", label: "Intensite chambres", kind: "select", options: [
      { value: "low", label: "Faible" },
      { value: "standard", label: "Standard" },
      { value: "high", label: "Forte" },
    ] },
    { name: "ecs_intensity_level", label: "Intensite ECS", kind: "select", required: true, options: [
      { value: "low", label: "Faible" },
      { value: "medium", label: "Moyenne" },
      { value: "high", label: "Forte" },
    ] },
    { name: "restaurant_active", label: "Restaurant actif", kind: "checkbox" },
    { name: "seminar_activity", label: "Seminaires / reunions", kind: "checkbox" },
  ],
  solutions: [
    { name: "selected_solution_codes", label: "Solutions retenues", kind: "csv", required: true, helper: "Codes separes par des virgules." },
    { name: "target_bacs_class", label: "Classe BACS cible", kind: "select", options: [
      { value: "A", label: "A" },
      { value: "B", label: "B" },
      { value: "C", label: "C" },
      { value: "D", label: "D" },
    ] },
    { name: "automation_package", label: "Bouquet automation", kind: "select", options: [
      { value: "standard", label: "Standard" },
      { value: "advanced", label: "Avance" },
      { value: "custom", label: "Personnalise" },
    ] },
  ],
  scenarios: [
    { name: "reference_scenario_name", label: "Scenario de reference", kind: "text", required: true },
    { name: "improvement_scenario_name", label: "Scenario d'amelioration", kind: "text", required: true },
    { name: "comparison_horizon_years", label: "Horizon de comparaison", kind: "number" },
  ],
  review: [
    { name: "report_language", label: "Langue du rapport", kind: "select", options: [
      { value: "fr", label: "Francais" },
      { value: "en", label: "Anglais" },
    ] },
    { name: "include_executive_summary", label: "Inclure la synthese executive", kind: "checkbox" },
    { name: "include_assumptions_appendix", label: "Inclure l'annexe hypotheses", kind: "checkbox" },
    { name: "ready_for_report", label: "Revue confirmee", kind: "checkbox", required: true },
  ],
};

function toFormDefaults(fields: FieldDefinition[], payload: Record<string, unknown>): WizardDraftStepValues {
  return Object.fromEntries(
    fields.map((field) => {
      const value = payload[field.name];
      if (field.kind === "checkbox") return [field.name, Boolean(value)];
      if (field.kind === "csv") return [field.name, Array.isArray(value) ? value.join(", ") : ""];
      return [field.name, value == null ? "" : value];
    }),
  ) as WizardDraftStepValues;
}

function normalizePayload(fields: FieldDefinition[], values: WizardDraftStepValues) {
  return Object.fromEntries(
    fields.map((field) => {
      const value = values[field.name];
      if (field.kind === "number") return [field.name, value === "" || value == null ? null : Number(value)];
      if (field.kind === "checkbox") return [field.name, Boolean(value)];
      if (field.kind === "csv") {
        const items = String(value ?? "")
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean);
        return [field.name, items];
      }
      return [field.name, String(value ?? "").trim() || null];
    }),
  );
}

type WizardDraftStepFormProps = {
  projectId: string;
  stepCode: string;
  payload: Record<string, unknown>;
  onSaved?: () => Promise<unknown> | unknown;
};

export function WizardDraftStepForm({ projectId, stepCode, payload, onSaved }: WizardDraftStepFormProps) {
  const { token } = useAuthContext();
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [savedMessage, setSavedMessage] = useState<string | null>(null);
  const fields = useMemo(() => stepFields[stepCode] ?? [], [stepCode]);

  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<WizardDraftStepValues>({
    resolver: zodResolver(wizardDraftStepSchema),
    defaultValues: toFormDefaults(fields, payload),
  });

  useEffect(() => {
    reset(toFormDefaults(fields, payload));
  }, [fields, payload, reset]);

  const onSubmit = async (values: WizardDraftStepValues) => {
    setSubmitError(null);
    setSavedMessage(null);

    try {
      await saveStep(projectId, stepCode, normalizePayload(fields, values), token);
      setSavedMessage("Etape enregistree.");
      await onSaved?.();
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : "Enregistrement de l'etape impossible.");
    }
  };

  if (fields.length === 0) {
    return <FeedbackBlock tone="warning">Aucun formulaire n'est defini pour cette etape.</FeedbackBlock>;
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ display: "grid", gap: 18 }}>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 16 }}>
        {fields.map((field) => (
          <div key={field.name} style={{ display: "grid", gap: 6, gridColumn: field.kind === "textarea" ? "1 / -1" : undefined }}>
            <label htmlFor={`${stepCode}_${field.name}`} style={{ fontSize: 14, fontWeight: 600 }}>
              {field.label}{field.required ? " *" : ""}
            </label>
            {field.kind === "textarea" ? (
              <textarea id={`${stepCode}_${field.name}`} rows={4} {...register(field.name)} style={{ ...inputStyle, resize: "vertical" }} />
            ) : field.kind === "select" ? (
              <select id={`${stepCode}_${field.name}`} {...register(field.name)} style={inputStyle}>
                <option value="">Selectionner</option>
                {(field.options ?? []).map((option) => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            ) : field.kind === "checkbox" ? (
              <label style={{ display: "flex", alignItems: "center", gap: 10, minHeight: 40 }}>
                <input id={`${stepCode}_${field.name}`} type="checkbox" {...register(field.name)} />
                <span>Oui</span>
              </label>
            ) : (
              <input
                id={`${stepCode}_${field.name}`}
                type={field.kind === "number" ? "number" : "text"}
                step={field.kind === "number" ? "0.01" : undefined}
                {...register(field.name)}
                style={inputStyle}
              />
            )}
            {field.helper ? <div style={{ color: "#627084", fontSize: 13 }}>{field.helper}</div> : null}
            <FieldError>{String(errors[field.name]?.message ?? "")}</FieldError>
          </div>
        ))}
      </div>

      {submitError ? <FeedbackBlock tone="error" compact>{submitError}</FeedbackBlock> : null}
      {savedMessage ? <FeedbackBlock tone="success" compact>{savedMessage}</FeedbackBlock> : null}

      <div style={{ display: "flex", justifyContent: "flex-end" }}>
        <button
          type="submit"
          disabled={isSubmitting}
          style={{
            borderRadius: 8,
            border: "1px solid #14365d",
            background: "#14365d",
            color: "#fff",
            padding: "10px 14px",
            fontWeight: 700,
            cursor: isSubmitting ? "not-allowed" : "pointer",
          }}
        >
          {isSubmitting ? "Enregistrement..." : "Enregistrer l'etape"}
        </button>
      </div>
    </form>
  );
}
