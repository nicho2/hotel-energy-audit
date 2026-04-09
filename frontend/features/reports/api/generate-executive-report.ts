import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { GeneratedReportResponse } from "@/types/reports";

export async function generateExecutiveReport(
  calculationRunId: string,
  token?: string | null,
): Promise<ApiEnvelope<GeneratedReportResponse>> {
  return apiClient.post<GeneratedReportResponse>(`/api/v1/reports/executive/${calculationRunId}/generate`, undefined, token);
}
