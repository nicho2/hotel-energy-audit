import { ProjectHistoryPage } from "@/features/history/components/project-history-page";

export default async function Page({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const { projectId } = await params;
  return <ProjectHistoryPage projectId={projectId} />;
}
