export type Orientation = "north" | "south" | "east" | "west" | "mixed";

export type BuildingPayload = {
  name: string | null;
  construction_period: string | null;
  gross_floor_area_m2: number | null;
  heated_area_m2: number | null;
  cooled_area_m2: number | null;
  number_of_floors: number | null;
  number_of_rooms: number | null;
  main_orientation: Orientation | null;
  compactness_level: string | null;
  has_restaurant: boolean;
  has_meeting_rooms: boolean;
  has_spa: boolean;
  has_pool: boolean;
};

export type BuildingResponse = {
  id: string;
  project_id: string;
  name: string | null;
  construction_period: string | null;
  gross_floor_area_m2: number | null;
  heated_area_m2: number | null;
  cooled_area_m2: number | null;
  number_of_floors: number | null;
  number_of_rooms: number | null;
  main_orientation: Orientation | null;
  compactness_level: string | null;
  has_restaurant: boolean;
  has_meeting_rooms: boolean;
  has_spa: boolean;
  has_pool: boolean;
};
