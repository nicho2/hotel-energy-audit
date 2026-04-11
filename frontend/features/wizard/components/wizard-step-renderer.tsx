"use client";

import { BuildingStepForm } from "@/features/building/components/building-step-form";
import { BacsStepForm } from "@/features/bacs/components/bacs-step-form";
import { SystemsStepForm } from "@/features/systems/components/systems-step-form";
import { ZonesStepForm } from "@/features/zones/components/zones-step-form";
import type { WizardStep } from "@/types/wizard";
import { useI18n } from "@/providers/i18n-provider";

type WizardStepRendererProps = {
  projectId: string;
  step: WizardStep;
  onSaved?: () => Promise<unknown> | unknown;
};

export function WizardStepRenderer({ projectId, step, onSaved }: WizardStepRendererProps) {
  const { t } = useI18n();

  if (step.code === "building") {
    return <BuildingStepForm projectId={projectId} onSaved={onSaved} />;
  }

  if (step.code === "zones") {
    return <ZonesStepForm projectId={projectId} onSaved={onSaved} />;
  }

  if (step.code === "systems") {
    return <SystemsStepForm projectId={projectId} onSaved={onSaved} />;
  }

  if (step.code === "bacs") {
    return <BacsStepForm projectId={projectId} onSaved={onSaved} />;
  }

  return (
    <div style={{ display: "grid", gap: 12 }}>
      <div style={{ fontSize: 16, fontWeight: 600 }}>{step.name}</div>
      <div style={{ color: "#627084" }}>
        {t("wizard.placeholder")}
      </div>
    </div>
  );
}
