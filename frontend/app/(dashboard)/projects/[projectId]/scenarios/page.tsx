import { ScenariosPage } from "@/features/scenarios/components/scenarios-page";

export default async function Page({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const { projectId } = await params;
  return <ScenariosPage projectId={projectId} />;
}
