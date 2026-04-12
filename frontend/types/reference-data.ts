export type CountryProfile = {
  id: string;
  country_code: string;
  name_fr: string;
  name_en: string;
  regulatory_scope: string;
  currency_code: string;
  default_language: string;
};

export type ClimateZone = {
  id: string;
  country_profile_id: string;
  code: string;
  name_fr: string;
  name_en: string;
  heating_severity_index: number;
  cooling_severity_index: number;
  solar_exposure_index: number;
  is_default: boolean;
};
