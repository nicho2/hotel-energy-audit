"use client";

import { useState } from "react";
import { ApiError } from "@/lib/api-client/errors";
import { useWizard } from "../hooks/use-wizard";
import { validateStep } from "../api/validate-step";
import { WizardStepper } from "@/components/wizard/wizard-stepper";
import { WizardNavigation } from "@/components/wizard/wizard-navigation";
import { WizardSidebarSummary } from "@/components/wizard/wizard-sidebar-summary";
import { WizardStepRenderer } from "./wizard-step-renderer";
import { useAuthContext } from "@/providers/auth-provider";
import { useI18n } from "@/providers/i18n-provider";
import { FeedbackBlock } from "@/components/ui/feedback";
import { ProjectSectionNav } from "@/features/projects/components/project-section-nav";

export function WizardShell({ projectId }: { projectId: string }) {
  const { data, error, isLoading, refetch } = useWizard(projectId);
  const { token } = useAuthContext();
  const { t } = useI18n();
  const [activeStepCode, setActiveStepCode] = useState<string | null>(null);
  const [isMovingNext, setIsMovingNext] = useState(false);
  const [navigationError, setNavigationError] = useState<string | null>(null);

  if (isLoading) return <FeedbackBlock>{t("wizard.loading")}</FeedbackBlock>;
  if (error) return <FeedbackBlock tone="error">{t("wizard.error")}</FeedbackBlock>;

  const wizard = data?.data;
  if (!wizard) return <FeedbackBlock tone="warning">{t("wizard.unavailable")}</FeedbackBlock>;

  const activeStep =
    wizard.steps.find((step) => step.code === activeStepCode) ??
    wizard.steps.find((step) => step.step === wizard.current_step) ??
    wizard.steps[0];

  const currentIndex = wizard.steps.findIndex((step) => step.code === activeStep.code);
  const canGoPrevious = currentIndex > 0;
  const canGoNext = currentIndex < wizard.steps.length - 1;
  const stepTitle = `${activeStep.step}. ${activeStep.name}`;

  const goPrevious = () => {
    if (!canGoPrevious) return;
    setNavigationError(null);
    setActiveStepCode(wizard.steps[currentIndex - 1]?.code ?? activeStep.code);
  };

  const goNext = async () => {
    if (!canGoNext) return;

    setNavigationError(null);
    setIsMovingNext(true);
    try {
      await validateStep(projectId, activeStep.code, token);
      setActiveStepCode(wizard.steps[currentIndex + 1]?.code ?? activeStep.code);
    } catch (error) {
      setNavigationError(error instanceof ApiError ? error.message : t("wizard.validationError"));
    } finally {
      setIsMovingNext(false);
    }
  };

  return (
    <div style={{ display: "grid", gap: 20 }}>
      <ProjectSectionNav projectId={projectId} />
      <div style={{ display: "grid", gridTemplateColumns: "300px minmax(0, 1fr)", gap: 24 }}>
        <div style={{ display: "grid", gap: 16 }}>
          <WizardStepper
            steps={wizard.steps}
            activeStepCode={activeStep.code}
            onSelectStep={(stepCode) => setActiveStepCode(stepCode)}
          />
          <WizardSidebarSummary currentStep={activeStep} readiness={wizard.readiness} />
        </div>
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, background: "#fff", padding: 24, display: "grid", gap: 20 }}>
          <div style={{ display: "grid", gap: 6 }}>
            <div style={{ fontSize: 13, color: "#627084", textTransform: "uppercase", letterSpacing: 0 }}>
              Wizard
            </div>
            <h2 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>{stepTitle}</h2>
          </div>

          <WizardStepRenderer projectId={projectId} step={activeStep} onSaved={refetch} />

          {navigationError ? (
            <FeedbackBlock tone="error" compact>
              {navigationError}
            </FeedbackBlock>
          ) : null}

          <WizardNavigation
            canGoPrevious={canGoPrevious}
            canGoNext={canGoNext}
            onPrevious={goPrevious}
            onNext={goNext}
            isSaving={isMovingNext}
          />
        </div>
      </div>
    </div>
  );
}
