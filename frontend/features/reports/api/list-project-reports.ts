import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { GeneratedReportResponse } from "@/types/reports";

export async function listProjectReports(
  projectId: string,
  token?: string | null,
): Promise<ApiEnvelope<GeneratedReportResponse[]>> {
  return apiClient.get<GeneratedReportResponse[]>(`/api/v1/projects/${projectId}/reports`, token);
}
