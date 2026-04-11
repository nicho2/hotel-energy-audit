"use client";

import { useEffect, useMemo, useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { ApiError } from "@/lib/api-client/errors";
import { useProject } from "@/features/projects/hooks/use-project";
import { useSystems } from "@/features/systems/hooks/use-systems";
import { useZones } from "@/features/zones/hooks/use-zones";
import type { ScenarioResponse, ScenarioSolutionAssignment, SolutionCatalogItem, TargetScope } from "@/types/scenarios";
import { useScenarios } from "../hooks/use-scenarios";
import { useI18n } from "@/providers/i18n-provider";
import { FeedbackBlock, FieldError } from "@/components/ui/feedback";
import { ProjectSectionNav } from "@/features/projects/components/project-section-nav";
import {
  scenarioEditorSchema,
  scenarioSolutionSchema,
  type ScenarioEditorFormValues,
  type ScenarioSolutionFormValues,
} from "../schemas/scenario-schema";

const inputStyle = {
  width: "100%",
  borderRadius: 8,
  border: "1px solid #d1d5db",
  padding: "10px 12px",
  fontSize: 14,
  background: "#fff",
} as const;

function toScenarioFormValues(scenario?: ScenarioResponse | null): ScenarioEditorFormValues {
  return {
    name: scenario?.name ?? "",
    description: scenario?.description ?? "",
    scenario_type: scenario?.scenario_type ?? "custom",
    status: scenario?.status ?? "draft",
    is_reference: scenario?.is_reference ?? false,
  };
}

function toAssignmentFormValues(assignment?: ScenarioSolutionAssignment | null): ScenarioSolutionFormValues {
  return {
    target_scope: assignment?.target_scope ?? "project",
    target_zone_id: assignment?.target_zone_id ?? "",
    target_system_id: assignment?.target_system_id ?? "",
    quantity: assignment?.quantity?.toString() ?? "",
    unit_cost_override: assignment?.unit_cost_override?.toString() ?? "",
    capex_override: assignment?.capex_override?.toString() ?? "",
    maintenance_override: assignment?.maintenance_override?.toString() ?? "",
    gain_override_percent: assignment?.gain_override_percent?.toString() ?? "",
    notes: assignment?.notes ?? "",
    is_selected: assignment?.is_selected ?? true,
  };
}

function toNullableNumber(value: string) {
  const normalized = value.trim();
  return normalized.length > 0 ? Number(normalized) : null;
}

export function ScenariosPage({ projectId }: { projectId: string }) {
  const project = useProject(projectId);
  const { t } = useI18n();
  const zones = useZones(projectId);
  const systems = useSystems(projectId);
  const [selectedScenarioId, setSelectedScenarioId] = useState<string | null>(null);
  const scenarios = useScenarios(projectId, selectedScenarioId);
  const [selectedCatalogItem, setSelectedCatalogItem] = useState<SolutionCatalogItem | null>(null);
  const [editingAssignment, setEditingAssignment] = useState<ScenarioSolutionAssignment | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const scenarioForm = useForm<ScenarioEditorFormValues>({
    resolver: zodResolver(scenarioEditorSchema),
    defaultValues: toScenarioFormValues(null),
  });
  const assignmentForm = useForm<ScenarioSolutionFormValues>({
    resolver: zodResolver(scenarioSolutionSchema),
    defaultValues: toAssignmentFormValues(null),
  });

  const scenarioList = scenarios.scenarios.data?.data ?? [];
  const selectedScenario = scenarioList.find((item) => item.id === selectedScenarioId) ?? scenarioList[0] ?? null;
  const assignments = scenarios.scenarioSolutions.data?.data ?? [];
  const catalog = scenarios.catalog.data?.data ?? [];

  useEffect(() => {
    if (!selectedScenarioId && scenarioList[0]) {
      setSelectedScenarioId(scenarioList[0].id);
    }
  }, [scenarioList, selectedScenarioId]);

  useEffect(() => {
    scenarioForm.reset(toScenarioFormValues(selectedScenario));
  }, [scenarioForm, selectedScenario]);

  useEffect(() => {
    assignmentForm.reset(toAssignmentFormValues(editingAssignment));
  }, [assignmentForm, editingAssignment]);

  const groupedCatalog = useMemo(() => {
    const groups = new Map<string, SolutionCatalogItem[]>();
    for (const item of catalog) {
      const existing = groups.get(item.solution_family) ?? [];
      existing.push(item);
      groups.set(item.solution_family, existing);
    }
    return Array.from(groups.entries());
  }, [catalog]);

  const handleCreateScenario = async () => {
    setSubmitError(null);
    try {
      const response = await scenarios.createScenario.mutateAsync({
        name: `Scenario ${scenarioList.length + 1}`,
        description: null,
        scenario_type: "custom",
        derived_from_scenario_id: null,
        is_reference: false,
      });
      setSelectedScenarioId(response.data.id);
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("scenarios.createError"));
    }
  };

  const handleDuplicateScenario = async () => {
    if (!selectedScenario) return;
    setSubmitError(null);
    try {
      const response = await scenarios.duplicateScenario.mutateAsync({
        scenarioId: selectedScenario.id,
        payload: { name: `${selectedScenario.name} copy` },
      });
      setSelectedScenarioId(response.data.id);
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("scenarios.duplicateError"));
    }
  };

  const handleSaveScenario = scenarioForm.handleSubmit(async (values) => {
    if (!selectedScenario) return;
    setSubmitError(null);
    try {
      await scenarios.updateScenario.mutateAsync({
        scenarioId: selectedScenario.id,
        payload: {
          name: values.name.trim(),
          description: values.description.trim() || null,
          scenario_type: values.scenario_type,
          status: values.status,
          is_reference: values.is_reference,
        },
      });
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("scenarios.saveError"));
    }
  });

  const handleAddSolution = (item: SolutionCatalogItem) => {
    setSelectedCatalogItem(item);
    setEditingAssignment(null);
    assignmentForm.reset(
      toAssignmentFormValues({
        ...({
          id: "",
          scenario_id: selectedScenario?.id ?? "",
          solution_code: item.code,
          solution_name: item.name,
          solution_description: item.description,
          solution_family: item.solution_family,
          target_scope: item.target_scopes[0] ?? "project",
          target_zone_id: null,
          target_system_id: null,
          quantity: item.default_quantity,
          unit_cost_override: null,
          capex_override: null,
          maintenance_override: null,
          gain_override_percent: null,
          notes: null,
          is_selected: true,
          created_at: "",
          updated_at: "",
        } satisfies ScenarioSolutionAssignment),
      }),
    );
  };

  const handleEditAssignment = (assignment: ScenarioSolutionAssignment) => {
    setEditingAssignment(assignment);
    setSelectedCatalogItem(catalog.find((item) => item.code === assignment.solution_code) ?? null);
  };

  const handleSaveAssignment = assignmentForm.handleSubmit(async (values) => {
    if (!selectedScenario) return;
    const solutionCode = editingAssignment?.solution_code ?? selectedCatalogItem?.code;
    if (!solutionCode) return;

    setSubmitError(null);
    const payload = {
      target_scope: values.target_scope,
      target_zone_id: values.target_scope === "zone" ? values.target_zone_id || null : null,
      target_system_id: values.target_scope === "system" ? values.target_system_id || null : null,
      quantity: toNullableNumber(values.quantity),
      unit_cost_override: toNullableNumber(values.unit_cost_override),
      capex_override: toNullableNumber(values.capex_override),
      maintenance_override: toNullableNumber(values.maintenance_override),
      gain_override_percent: toNullableNumber(values.gain_override_percent),
      notes: values.notes.trim() || null,
      is_selected: values.is_selected,
    };

    try {
      if (editingAssignment) {
        await scenarios.updateAssignment.mutateAsync({
          scenarioId: selectedScenario.id,
          assignmentId: editingAssignment.id,
          payload,
        });
      } else {
        await scenarios.createAssignment.mutateAsync({
          scenarioId: selectedScenario.id,
          payload: { solution_code: solutionCode, ...payload },
        });
      }
      setEditingAssignment(null);
      setSelectedCatalogItem(null);
      assignmentForm.reset(toAssignmentFormValues(null));
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("scenarios.assignmentSaveError"));
    }
  });

  const handleDeleteAssignment = async (assignment: ScenarioSolutionAssignment) => {
    if (!selectedScenario) return;
    if (!window.confirm(t("scenarios.deleteConfirm", { name: assignment.solution_name }))) return;
    setSubmitError(null);
    try {
      await scenarios.deleteAssignment.mutateAsync({
        scenarioId: selectedScenario.id,
        assignmentId: assignment.id,
      });
      if (editingAssignment?.id === assignment.id) {
        setEditingAssignment(null);
        setSelectedCatalogItem(null);
        assignmentForm.reset(toAssignmentFormValues(null));
      }
    } catch (error) {
      setSubmitError(error instanceof ApiError ? error.message : t("scenarios.assignmentDeleteError"));
    }
  };

  if (project.isLoading || scenarios.scenarios.isLoading || scenarios.catalog.isLoading || zones.isLoading || systems.isLoading) {
    return <FeedbackBlock>{t("scenarios.loading")}</FeedbackBlock>;
  }

  return (
    <div style={{ display: "grid", gap: 20 }}>
      <ProjectSectionNav projectId={projectId} />
      <div style={{ display: "grid", gap: 6 }}>
        <div style={{ fontSize: 13, color: "#627084", textTransform: "uppercase", letterSpacing: 0 }}>{t("scenarios.title")}</div>
        <h1 style={{ margin: 0, fontSize: 30, fontWeight: 700 }}>{project.data?.data.name ?? t("scenarios.projectFallback")}</h1>
      </div>

      {submitError ? (
        <FeedbackBlock tone="error" compact>
          {submitError}
        </FeedbackBlock>
      ) : null}

      <div style={{ display: "grid", gridTemplateColumns: "320px minmax(0, 1fr)", gap: 20, alignItems: "start" }}>
        <aside style={{ display: "grid", gap: 16 }}>
          <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, display: "grid", gap: 12 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div style={{ fontSize: 18, fontWeight: 700 }}>{t("scenarios.listTitle")}</div>
              <button type="button" onClick={handleCreateScenario} disabled={scenarios.createScenario.isPending} style={{ borderRadius: 8, border: "1px solid #14365d", background: "#14365d", color: "#fff", padding: "8px 12px", fontWeight: 700, opacity: scenarios.createScenario.isPending ? 0.65 : 1 }}>
                {t("common.add")}
              </button>
            </div>

            {scenarioList.length === 0 ? (
              <div style={{ color: "#627084", fontSize: 14 }}>{t("scenarios.empty")}</div>
            ) : (
              <div style={{ display: "grid", gap: 10 }}>
                {scenarioList.map((scenario) => (
                  <button
                    key={scenario.id}
                    type="button"
                    onClick={() => setSelectedScenarioId(scenario.id)}
                    style={{
                      textAlign: "left",
                      borderRadius: 8,
                      border: `1px solid ${selectedScenario?.id === scenario.id ? "#14365d" : "#e5e7eb"}`,
                      background: selectedScenario?.id === scenario.id ? "#eff6ff" : "#fff",
                      padding: 14,
                      display: "grid",
                      gap: 6,
                    }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                      <span style={{ fontWeight: 700 }}>{scenario.name}</span>
                      {scenario.is_reference ? (
                        <span style={{ fontSize: 12, color: "#14365d", fontWeight: 700 }}>{t("common.reference")}</span>
                      ) : null}
                    </div>
                    <div style={{ fontSize: 13, color: "#627084" }}>{scenario.scenario_type} · {scenario.status}</div>
                    <div style={{ fontSize: 13, color: "#334155" }}>{scenario.description ?? t("common.noDescription")}</div>
                  </button>
                ))}
              </div>
            )}
          </section>

          <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, display: "grid", gap: 12 }}>
            <div style={{ fontSize: 18, fontWeight: 700 }}>{t("scenarios.catalogTitle")}</div>
            {groupedCatalog.map(([family, items]) => (
              <div key={family} style={{ display: "grid", gap: 8 }}>
                <div style={{ fontSize: 13, fontWeight: 700, color: "#627084", textTransform: "uppercase" }}>{family}</div>
                {items.map((item) => (
                  <button
                    key={item.code}
                    type="button"
                    onClick={() => handleAddSolution(item)}
                    disabled={!selectedScenario}
                    style={{ textAlign: "left", borderRadius: 8, border: "1px solid #e5e7eb", background: "#fff", padding: 12, display: "grid", gap: 4, opacity: selectedScenario ? 1 : 0.6 }}
                  >
                    <div style={{ fontWeight: 700 }}>{item.name}</div>
                    <div style={{ fontSize: 13, color: "#627084" }}>{item.description}</div>
                  </button>
                ))}
              </div>
            ))}
          </section>
        </aside>

        <div style={{ display: "grid", gap: 20 }}>
          {!selectedScenario ? (
            <section style={{ border: "1px dashed #cbd5e1", borderRadius: 8, padding: 24, textAlign: "center", color: "#627084" }}>
              {t("scenarios.selectOrCreate")}
            </section>
          ) : (
            <>
              <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 20, display: "grid", gap: 16 }}>
                <div style={{ display: "flex", justifyContent: "space-between", gap: 12, alignItems: "center" }}>
                  <div style={{ fontSize: 20, fontWeight: 700 }}>{t("scenarios.editorTitle")}</div>
                  <button type="button" onClick={handleDuplicateScenario} disabled={scenarios.duplicateScenario.isPending} style={{ borderRadius: 8, border: "1px solid #cbd5e1", background: "#fff", padding: "10px 14px", fontWeight: 700, opacity: scenarios.duplicateScenario.isPending ? 0.65 : 1 }}>
                    {t("common.duplicate")}
                  </button>
                </div>

                <form onSubmit={handleSaveScenario} style={{ display: "grid", gap: 16 }}>
                  <div style={{ display: "grid", gridTemplateColumns: "1.5fr 1fr 1fr", gap: 12 }}>
                    <label style={{ display: "grid", gap: 6 }}>
                      <input {...scenarioForm.register("name")} style={inputStyle} placeholder={t("scenarios.namePlaceholder")} />
                      <FieldError>{scenarioForm.formState.errors.name?.message}</FieldError>
                    </label>
                    <select {...scenarioForm.register("scenario_type")} style={inputStyle}>
                      <option value="baseline">baseline</option>
                      <option value="improved">improved</option>
                      <option value="target_bacs">target_bacs</option>
                      <option value="custom">custom</option>
                    </select>
                    <select {...scenarioForm.register("status")} style={inputStyle}>
                      <option value="draft">draft</option>
                      <option value="ready">ready</option>
                      <option value="archived">archived</option>
                    </select>
                  </div>

                  <textarea {...scenarioForm.register("description")} rows={3} style={{ ...inputStyle, resize: "vertical" }} placeholder={t("scenarios.descriptionPlaceholder")} />

                  <label style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 14, fontWeight: 600 }}>
                    <input type="checkbox" {...scenarioForm.register("is_reference")} />
                    {t("scenarios.referenceCheckbox")}
                  </label>

                  <div style={{ display: "flex", justifyContent: "flex-end" }}>
                    <button type="submit" disabled={scenarios.updateScenario.isPending} style={{ borderRadius: 8, border: "1px solid #14365d", background: "#14365d", color: "#fff", padding: "10px 14px", fontWeight: 700, opacity: scenarios.updateScenario.isPending ? 0.65 : 1 }}>
                      {t("scenarios.saveScenario")}
                    </button>
                  </div>
                </form>
              </section>

              <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 20, display: "grid", gap: 16 }}>
                <div style={{ fontSize: 20, fontWeight: 700 }}>{t("scenarios.selectedSolutions")}</div>
                {assignments.length === 0 ? (
                  <div style={{ color: "#627084" }}>{t("scenarios.noAssignments")}</div>
                ) : (
                  <div style={{ display: "grid", gap: 10 }}>
                    {assignments.map((assignment) => (
                      <div key={assignment.id} style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 14, display: "grid", gap: 8 }}>
                        <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                          <div>
                            <div style={{ fontWeight: 700 }}>{assignment.solution_name}</div>
                            <div style={{ fontSize: 13, color: "#627084" }}>{assignment.solution_family} · {assignment.target_scope}</div>
                          </div>
                          <div style={{ display: "flex", gap: 8 }}>
                            <button type="button" onClick={() => handleEditAssignment(assignment)} style={{ borderRadius: 8, border: "1px solid #cbd5e1", background: "#fff", padding: "8px 12px" }}>
                              {t("common.edit")}
                            </button>
                            <button type="button" onClick={() => handleDeleteAssignment(assignment)} style={{ borderRadius: 8, border: "1px solid #fecaca", background: "#fff", color: "#b91c1c", padding: "8px 12px" }}>
                              {t("common.delete")}
                            </button>
                          </div>
                        </div>
                        <div style={{ fontSize: 14, color: "#334155" }}>{assignment.solution_description}</div>
                      </div>
                    ))}
                  </div>
                )}
              </section>

              {(selectedCatalogItem || editingAssignment) ? (
                <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 20, display: "grid", gap: 16 }}>
                  <div style={{ fontSize: 20, fontWeight: 700 }}>
                    {editingAssignment ? t("scenarios.editAssignment") : t("scenarios.addAssignment", { name: selectedCatalogItem?.name ?? "" })}
                  </div>

                  <form onSubmit={handleSaveAssignment} style={{ display: "grid", gap: 16 }}>
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12 }}>
                      <select {...assignmentForm.register("target_scope")} style={inputStyle}>
                        <option value="project">project</option>
                        <option value="zone">zone</option>
                        <option value="system">system</option>
                      </select>

                      <select {...assignmentForm.register("target_zone_id")} style={inputStyle}>
                        <option value="">{t("scenarios.targetZone")}</option>
                        {(zones.data?.data ?? []).map((zone) => (
                          <option key={zone.id} value={zone.id}>{zone.name}</option>
                        ))}
                      </select>

                      <select {...assignmentForm.register("target_system_id")} style={inputStyle}>
                        <option value="">{t("scenarios.targetSystem")}</option>
                        {(systems.data?.data ?? []).map((system) => (
                          <option key={system.id} value={system.id}>{system.name}</option>
                        ))}
                      </select>
                    </div>

                    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: 12 }}>
                      <label style={{ display: "grid", gap: 6 }}>
                        <input {...assignmentForm.register("quantity")} style={inputStyle} placeholder={t("scenarios.quantity")} />
                        <FieldError>{assignmentForm.formState.errors.quantity?.message}</FieldError>
                      </label>
                      <label style={{ display: "grid", gap: 6 }}>
                        <input {...assignmentForm.register("unit_cost_override")} style={inputStyle} placeholder={t("scenarios.unitCostOverride")} />
                        <FieldError>{assignmentForm.formState.errors.unit_cost_override?.message}</FieldError>
                      </label>
                      <label style={{ display: "grid", gap: 6 }}>
                        <input {...assignmentForm.register("capex_override")} style={inputStyle} placeholder={t("scenarios.capexOverride")} />
                        <FieldError>{assignmentForm.formState.errors.capex_override?.message}</FieldError>
                      </label>
                      <label style={{ display: "grid", gap: 6 }}>
                        <input {...assignmentForm.register("maintenance_override")} style={inputStyle} placeholder={t("scenarios.maintenanceOverride")} />
                        <FieldError>{assignmentForm.formState.errors.maintenance_override?.message}</FieldError>
                      </label>
                    </div>

                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                      <label style={{ display: "grid", gap: 6 }}>
                        <input {...assignmentForm.register("gain_override_percent")} style={inputStyle} placeholder={t("scenarios.gainOverride")} />
                        <FieldError>{assignmentForm.formState.errors.gain_override_percent?.message}</FieldError>
                      </label>
                      <label style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 14, fontWeight: 600 }}>
                        <input type="checkbox" {...assignmentForm.register("is_selected")} />
                        {t("scenarios.activeSelection")}
                      </label>
                    </div>

                    <textarea {...assignmentForm.register("notes")} rows={3} style={{ ...inputStyle, resize: "vertical" }} placeholder={t("scenarios.notes")} />

                    <div style={{ display: "flex", justifyContent: "flex-end", gap: 12 }}>
                      <button
                        type="button"
                        onClick={() => {
                          setEditingAssignment(null);
                          setSelectedCatalogItem(null);
                          assignmentForm.reset(toAssignmentFormValues(null));
                        }}
                        style={{ borderRadius: 8, border: "1px solid #cbd5e1", background: "#fff", padding: "10px 14px", fontWeight: 700 }}
                      >
                        {t("common.cancel")}
                      </button>
                      <button type="submit" disabled={scenarios.createAssignment.isPending || scenarios.updateAssignment.isPending} style={{ borderRadius: 8, border: "1px solid #14365d", background: "#14365d", color: "#fff", padding: "10px 14px", fontWeight: 700, opacity: scenarios.createAssignment.isPending || scenarios.updateAssignment.isPending ? 0.65 : 1 }}>
                        {editingAssignment ? t("scenarios.saveAssignment") : t("scenarios.addToScenario")}
                      </button>
                    </div>
                  </form>
                </section>
              ) : null}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
