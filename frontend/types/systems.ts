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

export type TechnologyType =
  | "gas_boiler"
  | "oil_boiler"
  | "electric_boiler"
  | "heat_pump"
  | "chiller"
  | "dx_unit"
  | "ahu"
  | "cmv"
  | "storage_tank"
  | "instantaneous_heater"
  | "led"
  | "fluorescent"
  | "pump"
  | "fan"
  | "bms"
  | "other";

export type EfficiencyLevel = "low" | "standard" | "high" | "premium";

export type TechnicalSystemResponse = {
  id: string;
  project_id: string;
  name: string;
  system_type: SystemType;
  energy_source: EnergySource | null;
  technology_type: TechnologyType | null;
  efficiency_level: EfficiencyLevel | null;
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
  technology_type: TechnologyType | null;
  efficiency_level: EfficiencyLevel | null;
  serves: string | null;
  quantity: number | null;
  year_installed: number | null;
  is_primary: boolean;
  notes: string | null;
  order_index: number;
};

export type TechnicalSystemUpdatePayload = Partial<TechnicalSystemCreatePayload>;
