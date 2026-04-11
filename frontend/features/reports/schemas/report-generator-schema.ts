import { z } from "zod";

export const reportGeneratorSchema = z.object({
  scenario_id: z.string().min(1, "Selectionnez un scenario."),
  report_type: z.literal("executive"),
  branding_profile_id: z.string().trim().uuid().or(z.literal("")),
});

export type ReportGeneratorFormValues = z.infer<typeof reportGeneratorSchema>;
