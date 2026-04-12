export type BuildingType = "hotel" | "aparthotel" | "residence" | "other_accommodation";

export type ProjectListItem = {
  id: string;
  name: string;
  client_name: string | null;
  status: string;
  wizard_step: number | string;
  updated_at: string;
};

export type ProjectCreatePayload = {
  name: string;
  client_name: string | null;
  country_profile_id: string | null;
  climate_zone_id: string | null;
  building_type: BuildingType;
  project_goal: string | null;
  branding_profile_id: string | null;
  template_id?: string | null;
};

export type ProjectUpdatePayload = {
  name?: string;
  client_name?: string | null;
  reference_code?: string | null;
  description?: string | null;
  status?: string;
  wizard_step?: number;
  building_type?: BuildingType;
  project_goal?: string | null;
  country_profile_id?: string | null;
  climate_zone_id?: string | null;
  branding_profile_id?: string | null;
};

export type ProjectResponse = {
  id: string;
  organization_id: string;
  created_by_user_id: string;
  template_id: string | null;
  name: string;
  client_name: string | null;
  reference_code: string | null;
  description: string | null;
  status: string;
  wizard_step: number;
  building_type: BuildingType;
  project_goal: string | null;
  country_profile_id: string | null;
  climate_zone_id: string | null;
  branding_profile_id: string | null;
  created_at: string;
  updated_at: string;
};

export type ProjectOverviewCard = {
  key: string;
  label: string;
  value: string;
  helper: string;
};
