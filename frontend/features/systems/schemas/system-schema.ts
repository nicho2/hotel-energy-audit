import { z } from "zod";

const currentYear = new Date().getFullYear();

export const systemTypeSchema = z.enum([
  "heating",
  "cooling",
  "ventilation",
  "dhw",
  "lighting",
  "auxiliaries",
  "control",
]);

export const energySourceSchema = z.enum([
  "electricity",
  "natural_gas",
  "fuel_oil",
  "district_heating",
  "district_cooling",
  "lpg",
  "biomass",
  "solar",
  "ambient",
  "other",
]);

export const technologyTypeSchema = z.enum([
  "gas_boiler",
  "oil_boiler",
  "electric_boiler",
  "heat_pump",
  "chiller",
  "dx_unit",
  "ahu",
  "cmv",
  "storage_tank",
  "instantaneous_heater",
  "led",
  "fluorescent",
  "pump",
  "fan",
  "bms",
  "other",
]);

export const efficiencyLevelSchema = z.enum(["low", "standard", "high", "premium"]);

const nullableIntegerString = z
  .string()
  .trim()
  .refine((value) => value.length === 0 || (Number.isInteger(Number(value)) && Number(value) >= 1), "Saisir un entier superieur ou egal a 1.");

const nullableYearString = z
  .string()
  .trim()
  .refine(
    (value) =>
      value.length === 0 ||
      (Number.isInteger(Number(value)) && Number(value) >= 1900 && Number(value) <= currentYear + 1),
    `Saisir une annee entre 1900 et ${currentYear + 1}.`,
  );

const nonNegativeIntegerString = z
  .string()
  .trim()
  .min(1, "Ce champ est requis.")
  .refine((value) => Number.isInteger(Number(value)) && Number(value) >= 0, "Saisir un entier positif ou nul.");

export const systemEditorSchema = z.object({
  name: z.string().trim().min(1, "Le nom est requis.").max(255, "Le nom est trop long."),
  system_type: systemTypeSchema,
  energy_source: z.union([energySourceSchema, z.literal("")]),
  technology_type: z.union([technologyTypeSchema, z.literal("")]),
  efficiency_level: z.union([efficiencyLevelSchema, z.literal("")]),
  serves: z.string().trim().max(255, "Le champ est trop long."),
  quantity: nullableIntegerString,
  year_installed: nullableYearString,
  is_primary: z.boolean(),
  notes: z.string(),
  order_index: nonNegativeIntegerString,
});

export type SystemEditorFormValues = z.infer<typeof systemEditorSchema>;
