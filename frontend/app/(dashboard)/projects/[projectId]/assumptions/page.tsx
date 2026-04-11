import { AssumptionsPage } from "@/features/assumptions/components/assumptions-page";

export default async function Page({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const { projectId } = await params;
  return <AssumptionsPage projectId={projectId} />;
}
