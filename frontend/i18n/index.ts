import frAuth from "./fr/auth.json";
import frCommon from "./fr/common.json";
import frCompare from "./fr/compare.json";
import frProjects from "./fr/projects.json";
import frReports from "./fr/reports.json";
import frScenarios from "./fr/scenarios.json";
import frWizard from "./fr/wizard.json";
import enAuth from "./en/auth.json";
import enCommon from "./en/common.json";
import enCompare from "./en/compare.json";
import enProjects from "./en/projects.json";
import enReports from "./en/reports.json";
import enScenarios from "./en/scenarios.json";
import enWizard from "./en/wizard.json";

export const supportedLanguages = ["fr", "en"] as const;

export type Language = (typeof supportedLanguages)[number];
export type TranslationDictionary = Record<string, string>;

export const dictionaries: Record<Language, TranslationDictionary> = {
  fr: {
    ...frCommon,
    ...frAuth,
    ...frProjects,
    ...frWizard,
    ...frScenarios,
    ...frCompare,
    ...frReports,
  },
  en: {
    ...enCommon,
    ...enAuth,
    ...enProjects,
    ...enWizard,
    ...enScenarios,
    ...enCompare,
    ...enReports,
  },
};

export function isLanguage(value: string): value is Language {
  return supportedLanguages.includes(value as Language);
}
