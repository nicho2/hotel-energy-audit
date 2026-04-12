"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { ApiError } from "@/lib/api-client/errors";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { BrandingSelect } from "@/features/branding/components/branding-select";
import { useBrandingProfiles } from "@/features/branding/hooks/use-branding-profiles";
import { useClimateZones } from "@/features/reference-data/hooks/use-climate-zones";
import { useCountryProfiles } from "@/features/reference-data/hooks/use-country-profiles";
import { useCreateProject } from "../hooks/use-create-project";
import { buildingTypeOptions, projectSchema, type ProjectFormValues } from "../schemas/project-schema";
import type { ProjectCreatePayload } from "@/types/project";
import { useI18n } from "@/providers/i18n-provider";

function toNullableValue(value?: string) {
  const normalized = value?.trim() ?? "";
  return normalized.length > 0 ? normalized : null;
}

function toCreatePayload(values: ProjectFormValues): ProjectCreatePayload {
  return {
    name: values.name.trim(),
    client_name: toNullableValue(values.client_name),
    country_profile_id: values.country_profile_id,
    climate_zone_id: values.climate_zone_id,
    building_type: values.building_type,
    project_goal: toNullableValue(values.project_goal),
    branding_profile_id: toNullableValue(values.branding_profile_id),
  };
}

export function CreateProjectForm() {
  const router = useRouter();
  const createProject = useCreateProject();
  const brandingProfiles = useBrandingProfiles();
  const { t, language } = useI18n();
  const [submitError, setSubmitError] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<ProjectFormValues>({
    resolver: zodResolver(projectSchema),
    defaultValues: {
      name: "",
      client_name: "",
      country_profile_id: "",
      climate_zone_id: "",
      building_type: "hotel",
      project_goal: "",
      branding_profile_id: "",
    },
  });
  const selectedCountryProfileId = watch("country_profile_id");
  const selectedClimateZoneId = watch("climate_zone_id");
  const countryProfiles = useCountryProfiles();
  const climateZones = useClimateZones(selectedCountryProfileId);
  const countries = countryProfiles.data?.data ?? [];
  const zones = climateZones.data?.data ?? [];

  useEffect(() => {
    if (!selectedClimateZoneId || climateZones.isLoading) {
      return;
    }

    const climateZoneStillAvailable = zones.some((zone) => zone.id === selectedClimateZoneId);
    if (!climateZoneStillAvailable) {
      setValue("climate_zone_id", "", { shouldValidate: true });
    }
  }, [climateZones.isLoading, selectedClimateZoneId, setValue, zones]);

  const onSubmit = async (values: ProjectFormValues) => {
    setSubmitError(null);

    try {
      const response = await createProject.mutateAsync(toCreatePayload(values));
      router.push(`/projects/${response.data.id}`);
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("projects.form.createError"));
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ display: "grid", gap: 20, maxWidth: 720 }}>
      <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 24, display: "grid", gap: 16 }}>
        <div style={{ display: "grid", gap: 6 }}>
          <label htmlFor="name" style={{ fontSize: 14, fontWeight: 600 }}>{t("projects.form.name")}</label>
          <Input id="name" placeholder={t("projects.form.namePlaceholder")} {...register("name")} />
          {errors.name ? <p style={{ margin: 0, color: "#b91c1c", fontSize: 12 }}>{errors.name.message}</p> : null}
        </div>

        <div style={{ display: "grid", gap: 6 }}>
          <label htmlFor="client_name" style={{ fontSize: 14, fontWeight: 600 }}>{t("projects.form.client")}</label>
          <Input id="client_name" placeholder={t("projects.form.clientPlaceholder")} {...register("client_name")} />
          {errors.client_name ? <p style={{ margin: 0, color: "#b91c1c", fontSize: 12 }}>{errors.client_name.message}</p> : null}
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          <div style={{ display: "grid", gap: 6 }}>
            <label htmlFor="country_profile_id" style={{ fontSize: 14, fontWeight: 600 }}>{t("projects.form.countryProfile")}</label>
            <select
              id="country_profile_id"
              value={selectedCountryProfileId}
              disabled={countryProfiles.isLoading}
              onChange={(event) => {
                setValue("country_profile_id", event.target.value, { shouldValidate: true });
                setValue("climate_zone_id", "", { shouldValidate: true });
              }}
              style={{
                width: "100%",
                borderRadius: 8,
                border: "1px solid #d1d5db",
                padding: "10px 12px",
                fontSize: 14,
                background: "#fff",
              }}
            >
              <option value="">{countryProfiles.isLoading ? t("projects.form.referenceDataLoading") : t("projects.form.countryPlaceholder")}</option>
              {countries.map((country) => (
                <option key={country.id} value={country.id}>
                  {(language === "fr" ? country.name_fr : country.name_en) || country.name_fr} ({country.country_code})
                </option>
              ))}
            </select>
            {errors.country_profile_id ? <p style={{ margin: 0, color: "#b91c1c", fontSize: 12 }}>{errors.country_profile_id.message}</p> : null}
          </div>

          <div style={{ display: "grid", gap: 6 }}>
            <label htmlFor="climate_zone_id" style={{ fontSize: 14, fontWeight: 600 }}>{t("projects.form.climateZone")}</label>
            <select
              id="climate_zone_id"
              value={selectedClimateZoneId}
              disabled={!selectedCountryProfileId || climateZones.isLoading}
              onChange={(event) => setValue("climate_zone_id", event.target.value, { shouldValidate: true })}
              style={{
                width: "100%",
                borderRadius: 8,
                border: "1px solid #d1d5db",
                padding: "10px 12px",
                fontSize: 14,
                background: "#fff",
              }}
            >
              <option value="">
                {!selectedCountryProfileId
                  ? t("projects.form.countryFirst")
                  : climateZones.isLoading
                    ? t("projects.form.referenceDataLoading")
                    : t("projects.form.climatePlaceholder")}
              </option>
              {zones.map((zone) => (
                <option key={zone.id} value={zone.id}>
                  {(language === "fr" ? zone.name_fr : zone.name_en) || zone.name_fr} ({zone.code}){zone.is_default ? ` - ${t("projects.form.defaultClimate")}` : ""}
                </option>
              ))}
            </select>
            {errors.climate_zone_id ? <p style={{ margin: 0, color: "#b91c1c", fontSize: 12 }}>{errors.climate_zone_id.message}</p> : null}
          </div>
        </div>

        {countryProfiles.error || climateZones.error ? (
          <div style={{ border: "1px solid #fecaca", borderRadius: 8, background: "#fff", padding: 12, color: "#b91c1c", fontSize: 13 }}>
            {t("projects.form.referenceDataError")}
          </div>
        ) : null}

        <div style={{ display: "grid", gap: 6 }}>
          <label htmlFor="building_type" style={{ fontSize: 14, fontWeight: 600 }}>{t("projects.form.buildingType")}</label>
          <select
            id="building_type"
            {...register("building_type")}
            style={{
              width: "100%",
              borderRadius: 8,
              border: "1px solid #d1d5db",
              padding: "10px 12px",
              fontSize: 14,
              background: "#fff",
            }}
          >
            {buildingTypeOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {t(`projects.buildingTypes.${option.value}`)}
              </option>
            ))}
          </select>
          {errors.building_type ? <p style={{ margin: 0, color: "#b91c1c", fontSize: 12 }}>{errors.building_type.message}</p> : null}
        </div>

        <div style={{ display: "grid", gap: 6 }}>
          <label htmlFor="project_goal" style={{ fontSize: 14, fontWeight: 600 }}>{t("projects.form.projectGoal")}</label>
          <Input id="project_goal" placeholder={t("projects.form.projectGoalPlaceholder")} {...register("project_goal")} />
          {errors.project_goal ? <p style={{ margin: 0, color: "#b91c1c", fontSize: 12 }}>{errors.project_goal.message}</p> : null}
        </div>

        <div style={{ display: "grid", gap: 6 }}>
          <label htmlFor="branding_profile_id" style={{ fontSize: 14, fontWeight: 600 }}>{t("branding.selectLabel")}</label>
          <BrandingSelect
            id="branding_profile_id"
            value={watch("branding_profile_id")}
            profiles={brandingProfiles.data?.data ?? []}
            disabled={brandingProfiles.isLoading}
            onChange={(brandingProfileId) => setValue("branding_profile_id", brandingProfileId, { shouldValidate: true })}
          />
          <p style={{ margin: 0, color: "#627084", fontSize: 12 }}>
            {(brandingProfiles.data?.data ?? []).length > 0 ? t("branding.projectBranding") : t("branding.noProfiles")}
          </p>
          {errors.branding_profile_id ? <p style={{ margin: 0, color: "#b91c1c", fontSize: 12 }}>{errors.branding_profile_id.message}</p> : null}
        </div>
      </div>

      {submitError ? (
        <div style={{ border: "1px solid #fecaca", borderRadius: 12, background: "#fff", padding: 16, color: "#b91c1c" }}>
          {submitError}
        </div>
      ) : null}

      <div style={{ display: "flex", justifyContent: "flex-end" }}>
        <Button type="submit" disabled={createProject.isPending}>
          {createProject.isPending ? t("projects.form.creating") : t("projects.form.create")}
        </Button>
      </div>
    </form>
  );
}
