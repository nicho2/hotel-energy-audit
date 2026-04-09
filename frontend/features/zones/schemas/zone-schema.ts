import { z } from "zod";

const orientationSchema = z.enum(["north", "south", "east", "west", "mixed"]);
const zoneTypeSchema = z.enum([
  "guest_rooms",
  "circulation",
  "lobby",
  "restaurant",
  "meeting",
  "technical",
  "spa",
  "pool",
  "other",
]);

const positiveNumberString = z
  .string()
  .trim()
  .min(1, "Ce champ est requis.")
  .refine((value) => !Number.isNaN(Number(value)) && Number(value) > 0, "Saisir une valeur superieure a 0.");

const nonNegativeIntegerString = z
  .string()
  .trim()
  .min(1, "Ce champ est requis.")
  .refine(
    (value) => Number.isInteger(Number(value)) && Number(value) >= 0,
    "Saisir un entier positif ou nul.",
  );

export const zoneEditorSchema = z
  .object({
    name: z.string().trim().min(1, "Le nom est requis.").max(255, "Le nom est trop long."),
    zone_type: zoneTypeSchema,
    orientation: orientationSchema,
    area_m2: positiveNumberString,
    room_count: nonNegativeIntegerString,
    order_index: nonNegativeIntegerString,
  })
  .superRefine((value, ctx) => {
    if (value.zone_type !== "guest_rooms" && Number(value.room_count) !== 0) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Les zones hors chambres doivent avoir 0 chambre.",
        path: ["room_count"],
      });
    }
  });

export const zoneGenerationSchema = z
  .object({
    north_rooms: nonNegativeIntegerString,
    east_rooms: nonNegativeIntegerString,
    south_rooms: nonNegativeIntegerString,
    west_rooms: nonNegativeIntegerString,
    mixed_rooms: nonNegativeIntegerString,
    average_room_area_m2: positiveNumberString,
    total_guest_room_area_m2: z
      .string()
      .trim()
      .refine(
        (value) => value.length === 0 || (!Number.isNaN(Number(value)) && Number(value) > 0),
        "Saisir une valeur superieure a 0.",
      ),
    replace_existing: z.boolean(),
  })
  .superRefine((value, ctx) => {
    const totalRooms =
      Number(value.north_rooms) +
      Number(value.east_rooms) +
      Number(value.south_rooms) +
      Number(value.west_rooms) +
      Number(value.mixed_rooms);

    if (totalRooms <= 0) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Au moins une chambre doit etre repartie.",
        path: ["north_rooms"],
      });
    }
  });

export type ZoneEditorFormValues = z.infer<typeof zoneEditorSchema>;
export type ZoneGenerationFormValues = z.infer<typeof zoneGenerationSchema>;
