import { z } from "zod";

export const projectTemplateSchema = z.object({
  name: z.string().trim().min(3, "Le nom doit contenir au moins 3 caracteres.").max(255),
  description: z.string().trim().max(500).optional().or(z.literal("")),
  building_type: z.enum(["hotel", "aparthotel", "residence", "other_accommodation"]),
  country_profile_id: z.string().trim().uuid("Veuillez choisir un pays."),
  zoning_standard: z.string().trim().max(100).optional().or(z.literal("")),
  usage_standard: z.string().trim().max(100).optional().or(z.literal("")),
  favorite_solution_codes: z.string().trim().max(500).optional().or(z.literal("")),
});

export type ProjectTemplateFormValues = z.infer<typeof projectTemplateSchema>;

export const applyTemplateSchema = z.object({
  name: z.string().trim().min(3, "Le nom doit contenir au moins 3 caracteres.").max(255),
  client_name: z.string().trim().max(255).optional().or(z.literal("")),
  climate_zone_id: z.string().trim().uuid("Veuillez choisir une zone climatique."),
});

export type ApplyTemplateFormValues = z.infer<typeof applyTemplateSchema>;
