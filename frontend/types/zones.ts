import type { Orientation } from "./building";

export type ZoneType =
  | "guest_rooms"
  | "circulation"
  | "lobby"
  | "restaurant"
  | "meeting"
  | "technical"
  | "spa"
  | "pool"
  | "other";

export type ValidationStatus = "ok" | "warning" | "error";

export type BuildingZoneResponse = {
  id: string;
  project_id: string;
  name: string;
  zone_type: ZoneType;
  orientation: Orientation;
  area_m2: number;
  room_count: number;
  order_index: number;
};

export type BuildingZoneCreatePayload = {
  name: string;
  zone_type: ZoneType;
  orientation: Orientation;
  area_m2: number;
  room_count: number;
  order_index: number;
};

export type BuildingZoneUpdatePayload = Partial<BuildingZoneCreatePayload>;

export type ZoneDistributionInput = {
  orientation: Orientation;
  room_count: number;
};

export type BuildingZoneGeneratePayload = {
  room_distribution: ZoneDistributionInput[];
  average_room_area_m2: number;
  total_guest_room_area_m2: number | null;
  replace_existing: boolean;
};

export type ZoneValidationItem = {
  code: string;
  status: ValidationStatus;
  message: string;
};

export type ZoneValidationResponse = {
  is_valid: boolean;
  checks: ZoneValidationItem[];
  warnings: ZoneValidationItem[];
};
