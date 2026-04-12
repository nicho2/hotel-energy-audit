"use client";

import { useEffect, useMemo, useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { ApiError } from "@/lib/api-client/errors";
import { useAuthContext } from "@/providers/auth-provider";
import { useI18n } from "@/providers/i18n-provider";
import { FeedbackBlock, FieldError } from "@/components/ui/feedback";
import { useClimateZones } from "@/features/reference-data/hooks/use-climate-zones";
import { useCountryProfiles } from "@/features/reference-data/hooks/use-country-profiles";
import { saveStep } from "../api/save-step";
import { wizardDraftStepSchema, type WizardDraftStepValues } from "../schemas/wizard-draft-step-schema";

type FieldKind = "text" | "textarea" | "number" | "select" | "checkbox" | "csv";

type FieldDefinition = {
  name: string;
  labelKey: string;
  kind: FieldKind;
  required?: boolean;
  helperKey?: string;
  tooltipKey: string;
  options?: Array<{ value: string; labelKey: string }>;
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
    { name: "name", labelKey: "wizard.fields.project.name.label", tooltipKey: "wizard.fields.project.name.tooltip", kind: "text", required: true },
    { name: "client_name", labelKey: "wizard.fields.project.client_name.label", tooltipKey: "wizard.fields.project.client_name.tooltip", kind: "text" },
    { name: "reference_code", labelKey: "wizard.fields.project.reference_code.label", tooltipKey: "wizard.fields.project.reference_code.tooltip", kind: "text" },
    { name: "building_type", labelKey: "wizard.fields.project.building_type.label", tooltipKey: "wizard.fields.project.building_type.tooltip", kind: "select", required: true, options: [
      { value: "hotel", labelKey: "projects.buildingTypes.hotel" },
      { value: "aparthotel", labelKey: "projects.buildingTypes.aparthotel" },
      { value: "residence", labelKey: "projects.buildingTypes.residence" },
      { value: "other_accommodation", labelKey: "projects.buildingTypes.other_accommodation" },
    ] },
    { name: "project_goal", labelKey: "wizard.fields.project.project_goal.label", tooltipKey: "wizard.fields.project.project_goal.tooltip", kind: "text" },
    { name: "description", labelKey: "wizard.fields.project.description.label", tooltipKey: "wizard.fields.project.description.tooltip", kind: "textarea" },
  ],
  context: [
    { name: "country_profile_id", labelKey: "wizard.fields.context.country_profile_id.label", tooltipKey: "wizard.fields.context.country_profile_id.tooltip", kind: "select", required: true },
    { name: "climate_zone_id", labelKey: "wizard.fields.context.climate_zone_id.label", tooltipKey: "wizard.fields.context.climate_zone_id.tooltip", kind: "select", required: true },
    { name: "regulatory_frame", labelKey: "wizard.fields.context.regulatory_frame.label", tooltipKey: "wizard.fields.context.regulatory_frame.tooltip", kind: "text" },
    { name: "energy_price_electricity_eur_kwh", labelKey: "wizard.fields.context.energy_price_electricity_eur_kwh.label", tooltipKey: "wizard.fields.context.energy_price_electricity_eur_kwh.tooltip", kind: "number" },
    { name: "energy_price_gas_eur_kwh", labelKey: "wizard.fields.context.energy_price_gas_eur_kwh.label", tooltipKey: "wizard.fields.context.energy_price_gas_eur_kwh.tooltip", kind: "number" },
  ],
  usage: [
    { name: "average_occupancy_rate", labelKey: "wizard.fields.usage.average_occupancy_rate.label", tooltipKey: "wizard.fields.usage.average_occupancy_rate.tooltip", kind: "number", required: true, helperKey: "wizard.fields.usage.average_occupancy_rate.helper" },
    { name: "seasonality_profile", labelKey: "wizard.fields.usage.seasonality_profile.label", tooltipKey: "wizard.fields.usage.seasonality_profile.tooltip", kind: "select", options: [
      { value: "stable", labelKey: "wizard.options.seasonality.stable" },
      { value: "seasonal", labelKey: "wizard.options.seasonality.seasonal" },
      { value: "highly_seasonal", labelKey: "wizard.options.seasonality.highly_seasonal" },
    ] },
    { name: "room_usage_intensity", labelKey: "wizard.fields.usage.room_usage_intensity.label", tooltipKey: "wizard.fields.usage.room_usage_intensity.tooltip", kind: "select", options: [
      { value: "low", labelKey: "wizard.options.intensity.low" },
      { value: "standard", labelKey: "wizard.options.intensity.standard" },
      { value: "high", labelKey: "wizard.options.intensity.high" },
    ] },
    { name: "ecs_intensity_level", labelKey: "wizard.fields.usage.ecs_intensity_level.label", tooltipKey: "wizard.fields.usage.ecs_intensity_level.tooltip", kind: "select", required: true, options: [
      { value: "low", labelKey: "wizard.options.intensity.low" },
      { value: "medium", labelKey: "wizard.options.intensity.medium" },
      { value: "high", labelKey: "wizard.options.intensity.high" },
    ] },
    { name: "restaurant_active", labelKey: "wizard.fields.usage.restaurant_active.label", tooltipKey: "wizard.fields.usage.restaurant_active.tooltip", kind: "checkbox" },
    { name: "seminar_activity", labelKey: "wizard.fields.usage.seminar_activity.label", tooltipKey: "wizard.fields.usage.seminar_activity.tooltip", kind: "checkbox" },
  ],
  solutions: [
    { name: "selected_solution_codes", labelKey: "wizard.fields.solutions.selected_solution_codes.label", tooltipKey: "wizard.fields.solutions.selected_solution_codes.tooltip", kind: "csv", required: true, helperKey: "wizard.fields.solutions.selected_solution_codes.helper" },
    { name: "target_bacs_class", labelKey: "wizard.fields.solutions.target_bacs_class.label", tooltipKey: "wizard.fields.solutions.target_bacs_class.tooltip", kind: "select", options: [
      { value: "A", labelKey: "wizard.options.bacs.A" },
      { value: "B", labelKey: "wizard.options.bacs.B" },
      { value: "C", labelKey: "wizard.options.bacs.C" },
      { value: "D", labelKey: "wizard.options.bacs.D" },
    ] },
    { name: "automation_package", labelKey: "wizard.fields.solutions.automation_package.label", tooltipKey: "wizard.fields.solutions.automation_package.tooltip", kind: "select", options: [
      { value: "standard", labelKey: "wizard.options.package.standard" },
      { value: "advanced", labelKey: "wizard.options.package.advanced" },
      { value: "custom", labelKey: "wizard.options.package.custom" },
    ] },
  ],
  scenarios: [
    { name: "reference_scenario_name", labelKey: "wizard.fields.scenarios.reference_scenario_name.label", tooltipKey: "wizard.fields.scenarios.reference_scenario_name.tooltip", kind: "text", required: true },
    { name: "improvement_scenario_name", labelKey: "wizard.fields.scenarios.improvement_scenario_name.label", tooltipKey: "wizard.fields.scenarios.improvement_scenario_name.tooltip", kind: "text", required: true },
    { name: "comparison_horizon_years", labelKey: "wizard.fields.scenarios.comparison_horizon_years.label", tooltipKey: "wizard.fields.scenarios.comparison_horizon_years.tooltip", kind: "number" },
  ],
  review: [
    { name: "report_language", labelKey: "wizard.fields.review.report_language.label", tooltipKey: "wizard.fields.review.report_language.tooltip", kind: "select", options: [
      { value: "fr", labelKey: "wizard.options.language.fr" },
      { value: "en", labelKey: "wizard.options.language.en" },
    ] },
    { name: "include_executive_summary", labelKey: "wizard.fields.review.include_executive_summary.label", tooltipKey: "wizard.fields.review.include_executive_summary.tooltip", kind: "checkbox" },
    { name: "include_assumptions_appendix", labelKey: "wizard.fields.review.include_assumptions_appendix.label", tooltipKey: "wizard.fields.review.include_assumptions_appendix.tooltip", kind: "checkbox" },
    { name: "ready_for_report", labelKey: "wizard.fields.review.ready_for_report.label", tooltipKey: "wizard.fields.review.ready_for_report.tooltip", kind: "checkbox", required: true },
  ],
};

function toFormDefaults(fields: FieldDefinition[], payload: Record<string, unknown>): WizardDraftStepValues {
  return Object.fromEntries(
    fields.map((field) => {
      const value = payload[field.name];
      if (field.kind === "checkbox") return [field.name, Boolean(value)];
      if (field.kind === "csv") return [field.name, Array.isArray(value) ? value.join(", ") : ""];
      if (field.name === "average_occupancy_rate" && typeof value === "number" && value <= 1) {
        return [field.name, Math.round(value * 100).toString()];
      }
      return [field.name, value == null ? "" : value];
    }),
  ) as WizardDraftStepValues;
}

function normalizePayload(fields: FieldDefinition[], values: WizardDraftStepValues) {
  return Object.fromEntries(
    fields.map((field) => {
      const value = values[field.name];
      if (field.kind === "number") {
        if (value === "" || value == null) return [field.name, null];
        const numericValue = Number(value);
        if (field.name === "average_occupancy_rate") {
          return [field.name, numericValue > 1 ? numericValue / 100 : numericValue];
        }
        return [field.name, numericValue];
      }
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
  const { language, t } = useI18n();
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [savedMessage, setSavedMessage] = useState<string | null>(null);
  const fields = useMemo(() => stepFields[stepCode] ?? [], [stepCode]);

  const { register, handleSubmit, reset, setValue, watch, formState: { errors, isSubmitting } } = useForm<WizardDraftStepValues>({
    resolver: zodResolver(wizardDraftStepSchema),
    defaultValues: toFormDefaults(fields, payload),
  });
  const selectedCountryProfileId = String(watch("country_profile_id") ?? "");
  const selectedClimateZoneId = String(watch("climate_zone_id") ?? "");
  const countryProfiles = useCountryProfiles(stepCode === "context");
  const climateZones = useClimateZones(stepCode === "context" ? selectedCountryProfileId : null);
  const countries = countryProfiles.data?.data ?? [];
  const zones = climateZones.data?.data ?? [];

  useEffect(() => {
    reset(toFormDefaults(fields, payload));
  }, [fields, payload, reset]);

  useEffect(() => {
    if (stepCode !== "context" || !selectedClimateZoneId || climateZones.isLoading) {
      return;
    }

    const climateZoneStillAvailable = zones.some((zone) => zone.id === selectedClimateZoneId);
    if (!climateZoneStillAvailable) {
      setValue("climate_zone_id", "", { shouldValidate: true });
    }
  }, [climateZones.isLoading, selectedClimateZoneId, setValue, stepCode, zones]);

  const onSubmit = async (values: WizardDraftStepValues) => {
    setSubmitError(null);
    setSavedMessage(null);

    try {
      await saveStep(projectId, stepCode, normalizePayload(fields, values), token);
      setSavedMessage(t("wizard.stepSaved"));
      await onSaved?.();
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("wizard.stepSaveError"));
    }
  };

  if (fields.length === 0) {
    return <FeedbackBlock tone="warning">{t("wizard.noStepForm")}</FeedbackBlock>;
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ display: "grid", gap: 18 }}>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 16 }}>
        {fields.map((field) => (
          <div key={field.name} style={{ display: "grid", gap: 6, gridColumn: field.kind === "textarea" ? "1 / -1" : undefined }}>
            <label
              htmlFor={`${stepCode}_${field.name}`}
              title={t(field.tooltipKey)}
              style={{ fontSize: 14, fontWeight: 600, display: "inline-flex", alignItems: "center", gap: 6 }}
            >
              {t(field.labelKey)}{field.required ? " *" : ""}
              <span
                aria-label={t(field.tooltipKey)}
                style={{ border: "1px solid #cbd5e1", borderRadius: 8, color: "#627084", fontSize: 11, fontWeight: 700, lineHeight: "16px", textAlign: "center", width: 16, height: 16 }}
              >
                ?
              </span>
            </label>
            {stepCode === "context" && field.name === "country_profile_id" ? (
              <select
                id={`${stepCode}_${field.name}`}
                value={selectedCountryProfileId}
                disabled={countryProfiles.isLoading}
                onChange={(event) => {
                  setValue("country_profile_id", event.target.value, { shouldValidate: true });
                  setValue("climate_zone_id", "", { shouldValidate: true });
                }}
                style={inputStyle}
              >
                <option value="">{countryProfiles.isLoading ? t("wizard.loadingShort") : t("wizard.countryPlaceholder")}</option>
                {countries.map((country) => (
                  <option key={country.id} value={country.id}>
                    {(language === "fr" ? country.name_fr : country.name_en) || country.name_fr} ({country.country_code})
                  </option>
                ))}
              </select>
            ) : stepCode === "context" && field.name === "climate_zone_id" ? (
              <select
                id={`${stepCode}_${field.name}`}
                value={selectedClimateZoneId}
                disabled={!selectedCountryProfileId || climateZones.isLoading}
                onChange={(event) => setValue("climate_zone_id", event.target.value, { shouldValidate: true })}
                style={inputStyle}
              >
                <option value="">
                  {!selectedCountryProfileId
                    ? t("wizard.countryFirst")
                    : climateZones.isLoading
                      ? t("wizard.loadingShort")
                      : t("wizard.climatePlaceholder")}
                </option>
                {zones.map((zone) => (
                  <option key={zone.id} value={zone.id}>
                    {(language === "fr" ? zone.name_fr : zone.name_en) || zone.name_fr} ({zone.code})
                  </option>
                ))}
              </select>
            ) : field.kind === "textarea" ? (
              <textarea id={`${stepCode}_${field.name}`} rows={4} {...register(field.name)} style={{ ...inputStyle, resize: "vertical" }} />
            ) : field.kind === "select" ? (
              <select id={`${stepCode}_${field.name}`} {...register(field.name)} style={inputStyle}>
                <option value="">{t("wizard.selectPlaceholder")}</option>
                {(field.options ?? []).map((option) => (
                  <option key={option.value} value={option.value}>{t(option.labelKey)}</option>
                ))}
              </select>
            ) : field.kind === "checkbox" ? (
              <label style={{ display: "flex", alignItems: "center", gap: 10, minHeight: 40 }}>
                <input id={`${stepCode}_${field.name}`} type="checkbox" {...register(field.name)} />
                <span>{t("wizard.yes")}</span>
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
            {field.helperKey ? <div style={{ color: "#627084", fontSize: 13 }}>{t(field.helperKey)}</div> : null}
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
          {isSubmitting ? t("wizard.saving") : t("wizard.saveStep")}
        </button>
      </div>
    </form>
  );
}
