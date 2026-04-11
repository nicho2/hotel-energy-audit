import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { ProjectHistoryEvent } from "@/types/history";

export async function listProjectHistory(
  projectId: string,
  token?: string | null,
): Promise<ApiEnvelope<ProjectHistoryEvent[]>> {
  return apiClient.get<ProjectHistoryEvent[]>(`/api/v1/projects/${projectId}/history`, token);
}
