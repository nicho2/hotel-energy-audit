import { ProjectOverviewPanel } from "@/features/projects/components/project-overview-panel";

export default async function ProjectDetailPage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const { projectId } = await params;

  return <ProjectOverviewPanel projectId={projectId} />;
}
