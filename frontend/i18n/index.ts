import frAssumptions from "./fr/assumptions.json";
import frAdmin from "./fr/admin.json";
import frAuth from "./fr/auth.json";
import frCommon from "./fr/common.json";
import frCompare from "./fr/compare.json";
import frCatalog from "./fr/catalog.json";
import frHistory from "./fr/history.json";
import frProjects from "./fr/projects.json";
import frReports from "./fr/reports.json";
import frScenarios from "./fr/scenarios.json";
import frTemplates from "./fr/templates.json";
import frWizard from "./fr/wizard.json";
import enAssumptions from "./en/assumptions.json";
import enAdmin from "./en/admin.json";
import enAuth from "./en/auth.json";
import enCommon from "./en/common.json";
import enCompare from "./en/compare.json";
import enCatalog from "./en/catalog.json";
import enHistory from "./en/history.json";
import enProjects from "./en/projects.json";
import enReports from "./en/reports.json";
import enScenarios from "./en/scenarios.json";
import enTemplates from "./en/templates.json";
import enWizard from "./en/wizard.json";

export const supportedLanguages = ["fr", "en"] as const;

export type Language = (typeof supportedLanguages)[number];
export type TranslationDictionary = Record<string, string>;

export const dictionaries: Record<Language, TranslationDictionary> = {
  fr: {
    ...frAssumptions,
    ...frAdmin,
    ...frCommon,
    ...frCatalog,
    ...frAuth,
    ...frProjects,
    ...frWizard,
    ...frScenarios,
    ...frTemplates,
    ...frCompare,
    ...frHistory,
    ...frReports,
  },
  en: {
    ...enAssumptions,
    ...enAdmin,
    ...enCommon,
    ...enCatalog,
    ...enAuth,
    ...enProjects,
    ...enWizard,
    ...enScenarios,
    ...enTemplates,
    ...enCompare,
    ...enHistory,
    ...enReports,
  },
};

export function isLanguage(value: string): value is Language {
  return supportedLanguages.includes(value as Language);
}
