import { ReportsPage } from "@/features/reports/components/reports-page";

export default async function Page({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const { projectId } = await params;
  return <ReportsPage projectId={projectId} />;
}
