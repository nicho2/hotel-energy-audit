export type SystemType =
  | "heating"
  | "cooling"
  | "ventilation"
  | "dhw"
  | "lighting"
  | "auxiliaries"
  | "control";

export type EnergySource =
  | "electricity"
  | "natural_gas"
  | "fuel_oil"
  | "district_heating"
  | "district_cooling"
  | "lpg"
  | "biomass"
  | "solar"
  | "ambient"
  | "other";

export type TechnicalSystemResponse = {
  id: string;
  project_id: string;
  name: string;
  system_type: SystemType;
  energy_source: EnergySource | null;
  serves: string | null;
  quantity: number | null;
  year_installed: number | null;
  is_primary: boolean;
  notes: string | null;
  order_index: number;
};

export type TechnicalSystemCreatePayload = {
  name: string;
  system_type: SystemType;
  energy_source: EnergySource | null;
  serves: string | null;
  quantity: number | null;
  year_installed: number | null;
  is_primary: boolean;
  notes: string | null;
  order_index: number;
};

export type TechnicalSystemUpdatePayload = Partial<TechnicalSystemCreatePayload>;
