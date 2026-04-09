import { ComparePage } from "@/features/results/components/compare-page";

export default async function Page({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const { projectId } = await params;
  return <ComparePage projectId={projectId} />;
}
