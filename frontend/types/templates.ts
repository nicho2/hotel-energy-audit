import type { BuildingType } from "./project";

export type ProjectTemplate = {
  id: string;
  organization_id: string;
  name: string;
  description: string | null;
  building_type: BuildingType;
  country_profile_id: string;
  default_payload_json: Record<string, unknown>;
  is_active: boolean;
  created_by_user_id: string;
  created_at: string;
  updated_at: string;
};

export type ProjectTemplateCreatePayload = {
  name: string;
  description: string | null;
  building_type: BuildingType;
  country_profile_id: string;
  default_payload_json: Record<string, unknown>;
  is_active: boolean;
};
