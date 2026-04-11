"use client";

import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { dictionaries, isLanguage, type Language } from "@/i18n";
import { env } from "@/lib/config/env";

type TranslationParams = Record<string, string | number | boolean | null | undefined>;

type I18nContextValue = {
  language: Language;
  setLanguage: (language: Language) => void;
  t: (key: string, params?: TranslationParams) => string;
};

const storageKey = "hea.language";
const fallbackLanguage: Language = "fr";
const I18nContext = createContext<I18nContextValue | null>(null);

function resolveDefaultLanguage(): Language {
  if (typeof window !== "undefined") {
    const stored = window.localStorage.getItem(storageKey);
    if (stored && isLanguage(stored)) {
      return stored;
    }

    const browserLanguage = window.navigator.language.split("-")[0];
    if (isLanguage(browserLanguage)) {
      return browserLanguage;
    }
  }

  return isLanguage(env.defaultLanguage) ? env.defaultLanguage : fallbackLanguage;
}

function interpolate(value: string, params?: TranslationParams) {
  if (!params) {
    return value;
  }

  return value.replace(/\{\{(\w+)\}\}/g, (match, paramName: string) => {
    const replacement = params[paramName];
    return replacement === undefined || replacement === null ? match : String(replacement);
  });
}

export function I18nProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState<Language>(() => resolveDefaultLanguage());

  useEffect(() => {
    document.documentElement.lang = language;
    window.localStorage.setItem(storageKey, language);
  }, [language]);

  const value = useMemo<I18nContextValue>(() => {
    const dictionary = dictionaries[language];

    return {
      language,
      setLanguage: setLanguageState,
      t: (key, params) => {
        const translation = dictionary[key];

        if (!translation) {
          const missing = `[[${key}]]`;
          if (process.env.NODE_ENV === "development") {
            console.warn(`Missing translation key: ${key}`);
          }
          return missing;
        }

        return interpolate(translation, params);
      },
    };
  }, [language]);

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n() {
  const context = useContext(I18nContext);

  if (!context) {
    throw new Error("useI18n must be used within I18nProvider.");
  }

  return context;
}
