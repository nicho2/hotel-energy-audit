# Frontend MVP

Base Next.js/TypeScript du MVP `hotel-energy-audit`.

## Scripts

- `npm install`
- `npm run dev`
- `npm run build`
- `npm run lint`

## Variables d'environnement

Copier `.env.example` en `.env.local` puis ajuster l'URL du backend si besoin.

## Structure cible

- `app/` : routes App Router et layouts minces
- `features/` : logique fonctionnelle par domaine
- `components/` : composants partages
- `i18n/` : dictionnaires FR/EN par domaine
- `lib/` : client API, config et utilitaires
- `providers/` : providers globaux
- `types/` : contrats TypeScript partages

## Internationalisation

Le provider `I18nProvider` charge les dictionnaires FR/EN, initialise la langue depuis la preference navigateur ou `NEXT_PUBLIC_DEFAULT_LANGUAGE`, puis persiste le choix localement. Les libelles d'interface doivent passer par `useI18n().t("domain.key")`; en developpement, une cle manquante s'affiche sous la forme `[[domain.key]]`.
