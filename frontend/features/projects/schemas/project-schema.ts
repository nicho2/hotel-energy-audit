import { z } from "zod";

export const buildingTypeOptions = [
  { value: "hotel", label: "Hotel" },
  { value: "aparthotel", label: "Aparthotel" },
  { value: "residence", label: "Residence" },
  { value: "other_accommodation", label: "Autre hebergement" },
] as const;

const optionalUuidField = z.string().trim().uuid("Veuillez saisir un UUID valide.").or(z.literal(""));
const requiredReferenceField = z.string().trim().uuid("Veuillez choisir une valeur dans la liste.");

export const projectSchema = z.object({
  name: z.string().trim().min(3, "Le nom doit contenir au moins 3 caracteres.").max(255),
  client_name: z.string().trim().max(255).optional().or(z.literal("")),
  country_profile_id: requiredReferenceField,
  climate_zone_id: requiredReferenceField,
  building_type: z.enum(["hotel", "aparthotel", "residence", "other_accommodation"]),
  project_goal: z.string().trim().max(100, "Le besoin doit rester concis.").optional().or(z.literal("")),
  branding_profile_id: optionalUuidField,
});

export type ProjectFormValues = z.infer<typeof projectSchema>;
