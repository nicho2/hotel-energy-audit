"use client";

import { useEffect, useMemo, useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { ApiError } from "@/lib/api-client/errors";
import { useAuthContext } from "@/providers/auth-provider";
import { useI18n } from "@/providers/i18n-provider";
import type { BacsClass } from "@/types/bacs";
import { useBacs } from "../hooks/use-bacs";
import { bacsStepSchema, type BacsStepFormValues } from "../schemas/bacs-schema";
import { BacsQuestionnaire } from "./bacs-questionnaire";
import { BacsSummaryCard } from "./bacs-summary-card";
import { MissingFunctionsPanel } from "./missing-functions-panel";

function toNullableString(value: string) {
  const normalized = value.trim();
  return normalized.length > 0 ? normalized : null;
}

function toFormValues(data?: {
  assessor_name?: string | null;
  manual_override_class?: BacsClass | null;
  notes?: string | null;
  functions?: Array<{ id: string; is_selected: boolean }>;
} | null): BacsStepFormValues {
  return {
    assessor_name: data?.assessor_name ?? "",
    manual_override_class: data?.manual_override_class ?? "",
    notes: data?.notes ?? "",
    selected_function_ids: (data?.functions ?? []).filter((item) => item.is_selected).map((item) => item.id),
  };
}

type BacsStepFormProps = {
  projectId: string;
  onSaved?: () => Promise<unknown> | unknown;
};

export function BacsStepForm({ projectId, onSaved }: BacsStepFormProps) {
  const { user } = useAuthContext();
  const { t } = useI18n();
  const bacs = useBacs(projectId);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const { register, handleSubmit, reset, setValue, watch, formState: { errors } } = useForm<BacsStepFormValues>({
    resolver: zodResolver(bacsStepSchema),
    defaultValues: toFormValues(null),
  });

  useEffect(() => {
    reset(toFormValues(bacs.current.data?.data));
  }, [bacs.current.data, reset]);

  const selectedFunctionIds = watch("selected_function_ids");
  const functions = bacs.current.data?.data.functions ?? [];
  const summary = bacs.summary.data?.data;
  const canManualOverride = user?.role === "org_admin";

  const selectionCount = useMemo(() => selectedFunctionIds.length, [selectedFunctionIds]);

  const toggleFunction = (functionId: string, nextSelected: boolean) => {
    const currentValues = watch("selected_function_ids");
    const nextValues = nextSelected
      ? Array.from(new Set([...currentValues, functionId]))
      : currentValues.filter((value) => value !== functionId);

    setValue("selected_function_ids", nextValues, { shouldDirty: true });
  };

  const onSubmit = async (values: BacsStepFormValues) => {
    setSubmitError(null);

    try {
      await bacs.saveAssessment.mutateAsync({
        assessor_name: toNullableString(values.assessor_name),
        manual_override_class: canManualOverride ? values.manual_override_class || null : null,
        notes: toNullableString(values.notes),
      });
      await bacs.saveFunctions.mutateAsync({
        selected_function_ids: values.selected_function_ids,
      });
      await Promise.all([bacs.current.refetch(), bacs.summary.refetch(), onSaved?.()]);
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("wizard.bacs.saveError"));
    }
  };

  const handleRefresh = async () => {
    setSubmitError(null);
    await Promise.all([bacs.current.refetch(), bacs.summary.refetch(), onSaved?.()]);
  };

  if (bacs.current.isLoading || bacs.summary.isLoading) {
    return <div>{t("wizard.bacs.loading")}</div>;
  }

  if (bacs.current.error || bacs.summary.error) {
    return (
      <div style={{ display: "grid", gap: 12 }}>
        <div style={{ border: "1px solid #fecaca", borderRadius: 12, background: "#fff", padding: 16, color: "#b91c1c" }}>
          {t("wizard.bacs.loadError")}
        </div>
        <div>
          <button
            type="button"
            onClick={handleRefresh}
            style={{ borderRadius: 10, border: "1px solid #14365d", background: "#fff", color: "#14365d", padding: "10px 14px", fontWeight: 600 }}
          >
            {t("wizard.bacs.reload")}
          </button>
        </div>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ display: "grid", gap: 20 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
        <div style={{ display: "grid", gap: 4 }}>
          <div style={{ fontSize: 14, color: "#627084", textTransform: "uppercase", letterSpacing: "0.04em" }}>
            BACS
          </div>
          <div style={{ fontSize: 16, color: "#334155" }}>
            {t("wizard.bacs.intro")}
          </div>
        </div>
        <button
          type="button"
          onClick={handleRefresh}
          disabled={bacs.current.isFetching || bacs.summary.isFetching}
          style={{ borderRadius: 10, border: "1px solid #cbd5e1", background: "#fff", padding: "10px 14px", fontWeight: 600 }}
        >
          {bacs.current.isFetching || bacs.summary.isFetching ? t("wizard.bacs.refreshing") : t("wizard.bacs.refresh")}
        </button>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "minmax(0, 1.4fr) minmax(320px, 0.9fr)", gap: 20, alignItems: "start" }}>
        <div style={{ display: "grid", gap: 16 }}>
          <section style={{ border: "1px solid #e5e7eb", borderRadius: 16, padding: 20, display: "grid", gap: 16 }}>
            <div style={{ display: "grid", gap: 4 }}>
              <div style={{ fontSize: 18, fontWeight: 700 }}>{t("wizard.bacs.questionnaireTitle")}</div>
              <div style={{ fontSize: 14, color: "#627084" }}>
                {t("wizard.bacs.selectionCount", { selected: selectionCount, total: functions.length })}
              </div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
              <div style={{ display: "grid", gap: 6 }}>
                <label htmlFor="bacs_assessor_name" style={{ fontSize: 14, fontWeight: 600 }}>{t("wizard.bacs.assessorName")}</label>
                <input
                  id="bacs_assessor_name"
                  {...register("assessor_name")}
                  style={{ width: "100%", borderRadius: 8, border: "1px solid #d1d5db", padding: "10px 12px", fontSize: 14, background: "#fff" }}
                />
                {errors.assessor_name ? <div style={{ color: "#b91c1c", fontSize: 13 }}>{errors.assessor_name.message}</div> : null}
              </div>

              <div style={{ display: "grid", gap: 6 }}>
                <label htmlFor="bacs_manual_override_class" style={{ fontSize: 14, fontWeight: 600 }}>{t("wizard.bacs.manualOverride")}</label>
                {canManualOverride ? (
                  <select
                    id="bacs_manual_override_class"
                    {...register("manual_override_class")}
                    style={{ width: "100%", borderRadius: 8, border: "1px solid #d1d5db", padding: "10px 12px", fontSize: 14, background: "#fff" }}
                  >
                    <option value="">{t("wizard.bacs.noOverride")}</option>
                    {["A", "B", "C", "D", "E"].map((item) => (
                      <option key={item} value={item}>{item}</option>
                    ))}
                  </select>
                ) : (
                  <div style={{ borderRadius: 8, border: "1px solid #e5e7eb", padding: "10px 12px", fontSize: 14, background: "#f8fafc", color: "#627084" }}>
                    {t("wizard.bacs.adminOnly")}
                  </div>
                )}
              </div>
            </div>

            <div style={{ display: "grid", gap: 6 }}>
              <label htmlFor="bacs_notes" style={{ fontSize: 14, fontWeight: 600 }}>{t("wizard.bacs.notes")}</label>
              <textarea
                id="bacs_notes"
                rows={4}
                {...register("notes")}
                style={{ width: "100%", borderRadius: 8, border: "1px solid #d1d5db", padding: "10px 12px", fontSize: 14, background: "#fff", resize: "vertical" }}
              />
            </div>
          </section>

          {functions.length === 0 ? (
            <section style={{ border: "1px dashed #cbd5e1", borderRadius: 16, padding: 24, textAlign: "center", color: "#627084" }}>
              {t("wizard.bacs.emptyCatalog")}
            </section>
          ) : (
            <BacsQuestionnaire functions={functions} selectedFunctionIds={selectedFunctionIds} onToggle={toggleFunction} />
          )}
        </div>

        <div style={{ display: "grid", gap: 16 }}>
          {summary ? <BacsSummaryCard summary={summary} /> : null}
          {summary ? <MissingFunctionsPanel functions={summary.top_missing_functions} /> : null}
        </div>
      </div>

      {submitError ? (
        <div style={{ border: "1px solid #fecaca", borderRadius: 12, background: "#fff", padding: 16, color: "#b91c1c" }}>
          {submitError}
        </div>
      ) : null}

      <div style={{ display: "flex", justifyContent: "flex-end" }}>
        <button
          type="submit"
          disabled={bacs.saveAssessment.isPending || bacs.saveFunctions.isPending}
          style={{
            borderRadius: 10,
            border: "1px solid #14365d",
            background: "#14365d",
            color: "#fff",
            padding: "10px 14px",
            fontWeight: 700,
            cursor: bacs.saveAssessment.isPending || bacs.saveFunctions.isPending ? "not-allowed" : "pointer",
          }}
        >
          {bacs.saveAssessment.isPending || bacs.saveFunctions.isPending ? t("wizard.saving") : t("wizard.bacs.save")}
        </button>
      </div>
    </form>
  );
}
