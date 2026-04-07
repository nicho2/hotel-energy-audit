import type { BuildingPayload, BuildingResponse } from "@/types/building";
import type { ApiEnvelope } from "@/types/api";
import { upsertBuilding } from "@/features/building/api/upsert-building";

export async function saveStep(
  projectId: string,
  stepCode: string,
  payload: unknown,
  token?: string | null,
): Promise<ApiEnvelope<BuildingResponse>> {
  // MVP scope: only the building step is backed by a dedicated save endpoint today.
  if (stepCode === "building") {
    return upsertBuilding(projectId, payload as BuildingPayload, token);
  }

  throw new Error(`Step '${stepCode}' is not saveable yet.`);
}
