import type { WizardReadiness, WizardStep } from "@/types/wizard";
import { useI18n } from "@/providers/i18n-provider";

type WizardSidebarSummaryProps = {
  currentStep?: WizardStep;
  readiness: WizardReadiness;
};

export function WizardSidebarSummary({ currentStep, readiness }: WizardSidebarSummaryProps) {
  const { t } = useI18n();

  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 16, display: "grid", gap: 12 }}>
      <div style={{ display: "grid", gap: 4 }}>
        <div style={{ fontSize: 12, color: "#627084", textTransform: "uppercase", letterSpacing: "0.04em" }}>
          {t("wizard.summary")}
        </div>
        <div style={{ fontWeight: 700, fontSize: 18 }}>{currentStep ? currentStep.name : "Wizard"}</div>
      </div>

      <div style={{ display: "grid", gap: 8, fontSize: 14, color: "#627084" }}>
        <div>{t("wizard.readinessStatus", { status: readiness.status })}</div>
        <div>{t("wizard.canCalculate", { value: readiness.can_calculate ? t("common.yes") : t("common.no") })}</div>
        <div>{t("wizard.blockingSteps", { steps: readiness.blocking_steps.join(", ") || t("common.emptyDash") })}</div>
      </div>
    </div>
  );
}
