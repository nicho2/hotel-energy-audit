import { apiClient } from "@/lib/api-client/client";
import type { ApiEnvelope } from "@/types/api";
import type { WizardState } from "@/types/wizard";

export async function getWizard(projectId: string, token?: string | null): Promise<ApiEnvelope<WizardState>> {
  return apiClient.get<WizardState>(`/api/v1/projects/${projectId}/wizard`, token);
}
