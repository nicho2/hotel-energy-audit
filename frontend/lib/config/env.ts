export const env = {
  apiBaseUrl: process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000",
  defaultLanguage: process.env.NEXT_PUBLIC_DEFAULT_LANGUAGE ?? "fr",
  appName: process.env.NEXT_PUBLIC_APP_NAME ?? "Hotel Energy Audit",
  authStorageKey: process.env.NEXT_PUBLIC_AUTH_STORAGE_KEY ?? "hea.auth",
};
