"use client";

import { BuildingStepForm } from "@/features/building/components/building-step-form";
import { BacsStepForm } from "@/features/bacs/components/bacs-step-form";
import { SystemsStepForm } from "@/features/systems/components/systems-step-form";
import { ZonesStepForm } from "@/features/zones/components/zones-step-form";
import type { WizardStep } from "@/types/wizard";
import { WizardDraftStepForm } from "./wizard-draft-step-form";

type WizardStepRendererProps = {
  projectId: string;
  step: WizardStep;
  stepPayload?: Record<string, unknown>;
  onSaved?: () => Promise<unknown> | unknown;
};

export function WizardStepRenderer({ projectId, step, stepPayload = {}, onSaved }: WizardStepRendererProps) {
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

  return <WizardDraftStepForm projectId={projectId} stepCode={step.code} payload={stepPayload} onSaved={onSaved} />;
}
