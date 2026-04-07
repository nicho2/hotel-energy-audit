import type { WizardReadiness, WizardStep } from "@/types/wizard";

type WizardSidebarSummaryProps = {
  currentStep?: WizardStep;
  readiness: WizardReadiness;
};

export function WizardSidebarSummary({ currentStep, readiness }: WizardSidebarSummaryProps) {
  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 16, display: "grid", gap: 12 }}>
      <div style={{ display: "grid", gap: 4 }}>
        <div style={{ fontSize: 12, color: "#627084", textTransform: "uppercase", letterSpacing: "0.04em" }}>
          Resume
        </div>
        <div style={{ fontWeight: 700, fontSize: 18 }}>{currentStep ? currentStep.name : "Wizard"}</div>
      </div>

      <div style={{ display: "grid", gap: 8, fontSize: 14, color: "#627084" }}>
        <div>Statut readiness: {readiness.status}</div>
        <div>Calcul activable: {readiness.can_calculate ? "oui" : "non"}</div>
        <div>Etapes bloquantes: {readiness.blocking_steps.join(", ") || "-"}</div>
      </div>
    </div>
  );
}
