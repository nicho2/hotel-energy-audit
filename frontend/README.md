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
- `lib/` : client API, config et utilitaires
- `providers/` : providers globaux
- `types/` : contrats TypeScript partages
