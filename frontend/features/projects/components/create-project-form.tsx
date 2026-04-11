"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { ApiError } from "@/lib/api-client/errors";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
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
    country_profile_id: toNullableValue(values.country_profile_id),
    climate_zone_id: toNullableValue(values.climate_zone_id),
    building_type: values.building_type,
    project_goal: toNullableValue(values.project_goal),
  };
}

export function CreateProjectForm() {
  const router = useRouter();
  const createProject = useCreateProject();
  const { t } = useI18n();
  const [submitError, setSubmitError] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
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
    },
  });

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
            <label htmlFor="country_profile_id" style={{ fontSize: 14, fontWeight: 600 }}>{t("projects.form.countryProfileId")}</label>
            <Input id="country_profile_id" placeholder={t("projects.form.optionalUuid")} {...register("country_profile_id")} />
            {errors.country_profile_id ? <p style={{ margin: 0, color: "#b91c1c", fontSize: 12 }}>{errors.country_profile_id.message}</p> : null}
          </div>

          <div style={{ display: "grid", gap: 6 }}>
            <label htmlFor="climate_zone_id" style={{ fontSize: 14, fontWeight: 600 }}>{t("projects.form.climateZoneId")}</label>
            <Input id="climate_zone_id" placeholder={t("projects.form.optionalUuid")} {...register("climate_zone_id")} />
            {errors.climate_zone_id ? <p style={{ margin: 0, color: "#b91c1c", fontSize: 12 }}>{errors.climate_zone_id.message}</p> : null}
          </div>
        </div>

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
