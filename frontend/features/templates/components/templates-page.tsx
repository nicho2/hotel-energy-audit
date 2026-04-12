"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { FeedbackBlock, FieldError } from "@/components/ui/feedback";
import { useCreateProject } from "@/features/projects/hooks/use-create-project";
import { buildingTypeOptions } from "@/features/projects/schemas/project-schema";
import { useClimateZones } from "@/features/reference-data/hooks/use-climate-zones";
import { useCountryProfiles } from "@/features/reference-data/hooks/use-country-profiles";
import { ApiError } from "@/lib/api-client/errors";
import { useI18n } from "@/providers/i18n-provider";
import type { ProjectTemplate } from "@/types/templates";
import { useProjectTemplates } from "../hooks/use-project-templates";
import {
  applyTemplateSchema,
  projectTemplateSchema,
  type ApplyTemplateFormValues,
  type ProjectTemplateFormValues,
} from "../schemas/project-template-schema";

const inputStyle = {
  width: "100%",
  borderRadius: 8,
  border: "1px solid #d1d5db",
  padding: "10px 12px",
  fontSize: 14,
  background: "#fff",
} as const;

function toNullable(value?: string) {
  const normalized = value?.trim() ?? "";
  return normalized.length > 0 ? normalized : null;
}

function parseCsv(value?: string) {
  return (value ?? "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function getTemplateSummary(template: ProjectTemplate) {
  const payload = template.default_payload_json;
  return {
    zoning: typeof payload.zoning_standard === "string" ? payload.zoning_standard : "",
    usage: typeof payload.usage_standard === "string" ? payload.usage_standard : "",
    favorites: Array.isArray(payload.favorite_solution_codes) ? payload.favorite_solution_codes.length : 0,
  };
}

export function TemplatesPage() {
  const router = useRouter();
  const { t, language } = useI18n();
  const countries = useCountryProfiles();
  const { templates, createTemplate } = useProjectTemplates();
  const createProject = useCreateProject();
  const [selectedTemplateId, setSelectedTemplateId] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const templateList = templates.data?.data ?? [];
  const selectedTemplate = templateList.find((item) => item.id === selectedTemplateId) ?? templateList[0] ?? null;
  const climateZones = useClimateZones(selectedTemplate?.country_profile_id);

  const templateForm = useForm<ProjectTemplateFormValues>({
    resolver: zodResolver(projectTemplateSchema),
    defaultValues: {
      name: "",
      description: "",
      building_type: "hotel",
      country_profile_id: "",
      zoning_standard: "hotel_standard",
      usage_standard: "standard",
      favorite_solution_codes: "",
    },
  });
  const applyForm = useForm<ApplyTemplateFormValues>({
    resolver: zodResolver(applyTemplateSchema),
    defaultValues: {
      name: "",
      client_name: "",
      climate_zone_id: "",
    },
  });

  useEffect(() => {
    if (!selectedTemplateId && templateList[0]) {
      setSelectedTemplateId(templateList[0].id);
    }
  }, [selectedTemplateId, templateList]);

  useEffect(() => {
    if (!selectedTemplate) {
      applyForm.reset({ name: "", client_name: "", climate_zone_id: "" });
      return;
    }

    const defaultZone = (climateZones.data?.data ?? []).find((zone) => zone.is_default) ?? climateZones.data?.data?.[0];
    applyForm.reset({
      name: selectedTemplate.name,
      client_name: "",
      climate_zone_id: defaultZone?.id ?? "",
    });
  }, [applyForm, climateZones.data?.data, selectedTemplate]);

  const templatesByBuilding = useMemo(() => {
    const counts = new Map<string, number>();
    for (const template of templateList) {
      counts.set(template.building_type, (counts.get(template.building_type) ?? 0) + 1);
    }
    return Array.from(counts.entries()).sort((left, right) => left[0].localeCompare(right[0]));
  }, [templateList]);

  const handleCreateTemplate = templateForm.handleSubmit(async (values) => {
    setSubmitError(null);
    try {
      const response = await createTemplate.mutateAsync({
        name: values.name.trim(),
        description: toNullable(values.description),
        building_type: values.building_type,
        country_profile_id: values.country_profile_id,
        is_active: true,
        default_payload_json: {
          mode: "express",
          zoning_standard: values.zoning_standard?.trim() || "hotel_standard",
          usage_standard: values.usage_standard?.trim() || "standard",
          favorite_solution_codes: parseCsv(values.favorite_solution_codes),
        },
      });
      setSelectedTemplateId(response.data.id);
      templateForm.reset({
        name: "",
        description: "",
        building_type: "hotel",
        country_profile_id: "",
        zoning_standard: "hotel_standard",
        usage_standard: "standard",
        favorite_solution_codes: "",
      });
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("templates.createError"));
    }
  });

  const handleApplyTemplate = applyForm.handleSubmit(async (values) => {
    if (!selectedTemplate) {
      return;
    }

    setSubmitError(null);
    try {
      const response = await createProject.mutateAsync({
        name: values.name.trim(),
        client_name: toNullable(values.client_name),
        country_profile_id: selectedTemplate.country_profile_id,
        climate_zone_id: values.climate_zone_id,
        building_type: selectedTemplate.building_type,
        project_goal: "pre_audit",
        branding_profile_id: null,
        template_id: selectedTemplate.id,
      });
      router.push(`/projects/${response.data.id}/wizard`);
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("templates.applyError"));
    }
  });

  if (templates.isLoading || countries.isLoading) {
    return <FeedbackBlock>{t("templates.loading")}</FeedbackBlock>;
  }

  return (
    <div style={{ display: "grid", gap: 20 }}>
      <div style={{ display: "grid", gap: 6 }}>
        <div style={{ fontSize: 13, color: "#627084", textTransform: "uppercase", letterSpacing: 0 }}>{t("templates.kicker")}</div>
        <h1 style={{ margin: 0, fontSize: 30, fontWeight: 800 }}>{t("templates.title")}</h1>
        <p style={{ margin: 0, color: "#627084", maxWidth: 760 }}>{t("templates.subtitle")}</p>
      </div>

      {templates.error ? <FeedbackBlock tone="error">{t("templates.error")}</FeedbackBlock> : null}
      {submitError ? <FeedbackBlock tone="error">{submitError}</FeedbackBlock> : null}

      <section style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
        {templatesByBuilding.length === 0 ? (
          <span style={{ color: "#627084", fontSize: 14 }}>{t("templates.noStats")}</span>
        ) : templatesByBuilding.map(([buildingType, count]) => (
          <span key={buildingType} style={{ border: "1px solid #dbe4ee", borderRadius: 8, padding: "8px 10px", background: "#fff", fontSize: 13 }}>
            <strong>{t(`projects.buildingTypes.${buildingType}`)}</strong> - {count}
          </span>
        ))}
      </section>

      <div style={{ display: "grid", gridTemplateColumns: "minmax(0, 1.2fr) minmax(320px, 0.8fr)", gap: 20, alignItems: "start" }}>
        <section style={{ display: "grid", gap: 14 }}>
          {templateList.length === 0 ? (
            <FeedbackBlock>{t("templates.empty")}</FeedbackBlock>
          ) : templateList.map((template) => {
            const summary = getTemplateSummary(template);
            return (
              <button
                key={template.id}
                type="button"
                onClick={() => setSelectedTemplateId(template.id)}
                style={{
                  textAlign: "left",
                  border: `1px solid ${selectedTemplate?.id === template.id ? "#14365d" : "#e5e7eb"}`,
                  borderRadius: 8,
                  background: selectedTemplate?.id === template.id ? "#eff6ff" : "#fff",
                  padding: 16,
                  display: "grid",
                  gap: 10,
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                  <div>
                    <div style={{ fontWeight: 800, fontSize: 18 }}>{template.name}</div>
                    <div style={{ color: "#627084", fontSize: 13 }}>{t(`projects.buildingTypes.${template.building_type}`)}</div>
                  </div>
                  <span style={{ color: template.is_active ? "#166534" : "#92400e", fontSize: 13, fontWeight: 700 }}>
                    {template.is_active ? t("templates.active") : t("templates.inactive")}
                  </span>
                </div>
                <p style={{ margin: 0, color: "#334155" }}>{template.description ?? t("common.noDescription")}</p>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 8, color: "#627084", fontSize: 13 }}>
                  <span>{t("templates.zoning")} {summary.zoning || "-"}</span>
                  <span>{t("templates.usage")} {summary.usage || "-"}</span>
                  <span>{t("templates.favoriteSolutions")} {summary.favorites}</span>
                </div>
              </button>
            );
          })}
        </section>

        <aside style={{ display: "grid", gap: 18 }}>
          <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, background: "#fff", padding: 18, display: "grid", gap: 14 }}>
            <h2 style={{ margin: 0, fontSize: 20 }}>{t("templates.applyTitle")}</h2>
            {!selectedTemplate ? (
              <div style={{ color: "#627084" }}>{t("templates.selectFirst")}</div>
            ) : (
              <form onSubmit={handleApplyTemplate} style={{ display: "grid", gap: 12 }}>
                <label style={{ display: "grid", gap: 6 }}>
                  <span style={{ fontSize: 14, fontWeight: 700 }}>{t("templates.projectName")}</span>
                  <input {...applyForm.register("name")} style={inputStyle} />
                  <FieldError>{applyForm.formState.errors.name?.message}</FieldError>
                </label>
                <label style={{ display: "grid", gap: 6 }}>
                  <span style={{ fontSize: 14, fontWeight: 700 }}>{t("templates.clientName")}</span>
                  <input {...applyForm.register("client_name")} style={inputStyle} />
                  <FieldError>{applyForm.formState.errors.client_name?.message}</FieldError>
                </label>
                <label style={{ display: "grid", gap: 6 }}>
                  <span style={{ fontSize: 14, fontWeight: 700 }}>{t("templates.climateZone")}</span>
                  <select {...applyForm.register("climate_zone_id")} disabled={climateZones.isLoading} style={inputStyle}>
                    <option value="">{climateZones.isLoading ? t("common.loading") : t("templates.chooseClimate")}</option>
                    {(climateZones.data?.data ?? []).map((zone) => (
                      <option key={zone.id} value={zone.id}>
                        {(language === "fr" ? zone.name_fr : zone.name_en) || zone.name_fr} ({zone.code})
                      </option>
                    ))}
                  </select>
                  <FieldError>{applyForm.formState.errors.climate_zone_id?.message}</FieldError>
                </label>
                <Button type="submit" disabled={createProject.isPending || climateZones.isLoading}>
                  {createProject.isPending ? t("templates.applying") : t("templates.apply")}
                </Button>
              </form>
            )}
          </section>

          <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, background: "#fff", padding: 18, display: "grid", gap: 14 }}>
            <h2 style={{ margin: 0, fontSize: 20 }}>{t("templates.createTitle")}</h2>
            <form onSubmit={handleCreateTemplate} style={{ display: "grid", gap: 12 }}>
              <label style={{ display: "grid", gap: 6 }}>
                <span style={{ fontSize: 14, fontWeight: 700 }}>{t("templates.name")}</span>
                <input {...templateForm.register("name")} style={inputStyle} />
                <FieldError>{templateForm.formState.errors.name?.message}</FieldError>
              </label>
              <label style={{ display: "grid", gap: 6 }}>
                <span style={{ fontSize: 14, fontWeight: 700 }}>{t("templates.description")}</span>
                <textarea {...templateForm.register("description")} rows={3} style={{ ...inputStyle, resize: "vertical" }} />
                <FieldError>{templateForm.formState.errors.description?.message}</FieldError>
              </label>
              <select {...templateForm.register("building_type")} style={inputStyle}>
                {buildingTypeOptions.map((option) => (
                  <option key={option.value} value={option.value}>{t(`projects.buildingTypes.${option.value}`)}</option>
                ))}
              </select>
              <select {...templateForm.register("country_profile_id")} style={inputStyle}>
                <option value="">{t("templates.chooseCountry")}</option>
                {(countries.data?.data ?? []).map((country) => (
                  <option key={country.id} value={country.id}>
                    {(language === "fr" ? country.name_fr : country.name_en) || country.name_fr}
                  </option>
                ))}
              </select>
              <FieldError>{templateForm.formState.errors.country_profile_id?.message}</FieldError>
              <input {...templateForm.register("zoning_standard")} style={inputStyle} placeholder={t("templates.zoningPlaceholder")} />
              <input {...templateForm.register("usage_standard")} style={inputStyle} placeholder={t("templates.usagePlaceholder")} />
              <input {...templateForm.register("favorite_solution_codes")} style={inputStyle} placeholder={t("templates.favoritePlaceholder")} />
              <Button type="submit" disabled={createTemplate.isPending}>
                {createTemplate.isPending ? t("templates.creating") : t("templates.create")}
              </Button>
            </form>
          </section>
        </aside>
      </div>
    </div>
  );
}
