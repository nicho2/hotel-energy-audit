"use client";

import { useWizard } from "../hooks/use-wizard";
import { WizardStepper } from "@/components/wizard/wizard-stepper";

export function WizardShell({ projectId }: { projectId: string }) {
  const { data, isLoading } = useWizard(projectId);

  if (isLoading) return <div>Chargement du wizard...</div>;

  const wizard: any = (data as any)?.data;
  if (!wizard) return <div>Wizard indisponible.</div>;

  return (
    <div style={{ display: "grid", gridTemplateColumns: "300px 1fr", gap: 24 }}>
      <div>
        <WizardStepper steps={wizard.steps} />
      </div>
      <div style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", padding: 24 }}>
        <h2 style={{ fontSize: 24, fontWeight: 600, marginBottom: 16 }}>Étape {wizard.current_step}</h2>
        <div>Contenu de l’étape à brancher ici.</div>
      </div>
    </div>
  );
}
