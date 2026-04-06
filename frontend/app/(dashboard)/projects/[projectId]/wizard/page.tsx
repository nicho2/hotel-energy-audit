import { WizardShell } from "@/features/wizard/components/wizard-shell";

export default async function ProjectWizardPage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const { projectId } = await params;
  return <WizardShell projectId={projectId} />;
}
