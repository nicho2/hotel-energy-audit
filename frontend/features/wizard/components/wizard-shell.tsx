"use client";

import { useMemo, useState } from "react";
import { useWizard } from "../hooks/use-wizard";
import { validateStep } from "../api/validate-step";
import { WizardStepper } from "@/components/wizard/wizard-stepper";
import { WizardNavigation } from "@/components/wizard/wizard-navigation";
import { WizardSidebarSummary } from "@/components/wizard/wizard-sidebar-summary";
import { WizardStepRenderer } from "./wizard-step-renderer";

export function WizardShell({ projectId }: { projectId: string }) {
  const { data, error, isLoading, refetch } = useWizard(projectId);
  const [activeStepCode, setActiveStepCode] = useState<string | null>(null);
  const [isMovingNext, setIsMovingNext] = useState(false);

  if (isLoading) return <div>Chargement du wizard...</div>;
  if (error) return <div>Erreur de chargement du wizard.</div>;

  const wizard = data?.data;
  if (!wizard) return <div>Wizard indisponible.</div>;

  const activeStep =
    wizard.steps.find((step) => step.code === activeStepCode) ??
    wizard.steps.find((step) => step.step === wizard.current_step) ??
    wizard.steps[0];

  const currentIndex = wizard.steps.findIndex((step) => step.code === activeStep.code);
  const canGoPrevious = currentIndex > 0;
  const canGoNext = currentIndex < wizard.steps.length - 1;
  const stepTitle = useMemo(() => `${activeStep.step}. ${activeStep.name}`, [activeStep]);

  const goPrevious = () => {
    if (!canGoPrevious) return;
    setActiveStepCode(wizard.steps[currentIndex - 1]?.code ?? activeStep.code);
  };

  const goNext = async () => {
    if (!canGoNext) return;

    setIsMovingNext(true);
    try {
      await validateStep(projectId, activeStep.code);
      setActiveStepCode(wizard.steps[currentIndex + 1]?.code ?? activeStep.code);
    } finally {
      setIsMovingNext(false);
    }
  };

  return (
    <div style={{ display: "grid", gridTemplateColumns: "300px minmax(0, 1fr)", gap: 24 }}>
      <div style={{ display: "grid", gap: 16 }}>
        <WizardStepper
          steps={wizard.steps}
          activeStepCode={activeStep.code}
          onSelectStep={(stepCode) => setActiveStepCode(stepCode)}
        />
        <WizardSidebarSummary currentStep={activeStep} readiness={wizard.readiness} />
      </div>
      <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 24, display: "grid", gap: 20 }}>
        <div style={{ display: "grid", gap: 6 }}>
          <div style={{ fontSize: 13, color: "#627084", textTransform: "uppercase", letterSpacing: "0.04em" }}>
            Wizard
          </div>
          <h2 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>{stepTitle}</h2>
        </div>

        <WizardStepRenderer projectId={projectId} step={activeStep} onSaved={refetch} />

        <WizardNavigation
          canGoPrevious={canGoPrevious}
          canGoNext={canGoNext}
          onPrevious={goPrevious}
          onNext={goNext}
          isSaving={isMovingNext}
        />
      </div>
    </div>
  );
}
