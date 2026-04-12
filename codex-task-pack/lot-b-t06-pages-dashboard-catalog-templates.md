# Codex Task Template

## Metadata
- Task ID: LOT-B-T06
- Epic: Recalage MVP initial vs implémentation actuelle
- Feature: Dashboard Catalog + Templates
- Priority: P1
- Owner: Frontend (+ Backend si templates absents)
- Status: todo
- Related files:
  - `frontend/app/(dashboard)/catalog/page.tsx`
  - `frontend/app/(dashboard)/templates/page.tsx`
  - `frontend/features/scenarios/**`
  - `frontend/features/projects/**`
  - `backend/app/api/v1/endpoints/*` (si besoin)
- Dependencies:
  - LOT-A-T02

## Context
Le menu global prévoit `Catalog` et `Templates`, mais les pages correspondantes sont encore des placeholders.
Les specs 5 et 7 attendent une expérience exploitable sur ces modules (comparaison de solutions et création depuis modèle).
Cette tâche rend ces entrées réellement utilisables.

## Objective
Implémenter des pages fonctionnelles pour le catalogue de solutions et les modèles de projet.

## In scope
- Catalog: listing, recherche/filtrage, visualisation des familles et impacts.
- Templates: listing, création basique, application à un nouveau projet.
- Connexion aux endpoints backend existants ou à créer (minimum MVP).
- Gestion des états loading/empty/error et i18n.

## Out of scope
- Éditeur avancé de templates versionnés.
- Personnalisation exhaustive du catalogue par rôle.

## Inputs / references
- `AGENTS.md`
- `docs/5-Specification-fonctionnelle-des-ecrans-et-du-wizard.md`
- `docs/7-Architecture-fonctionnelle-detaillee-des-API-backend.md`
- Additional docs:
  - `docs/0-cahier-des-charges-initial.md`

## Implementation notes
- Garder pages fines; logique dans `features/*`.
- Réutiliser hooks React Query déjà présents (`features/scenarios/api/list-solution-catalog.ts`).
- Rebouclage:
  1. Vérifier couverture des actions attendues par specs 5.
  2. Vérifier cohérence avec APIs disponibles réelles.
  3. Ajuster UX pour rester en mode express par défaut.

## Acceptance criteria
- [ ] `/catalog` et `/templates` ne sont plus des placeholders.
- [ ] Les données sont réellement chargées depuis backend.
- [ ] Les actions principales MVP sont accessibles (consulter, filtrer, créer/appliquer template).

## Tests to add or update
- [ ] Tests frontend des composants principaux des deux pages.
- [ ] Tests d’intégration API-client pour chargement/erreurs.

## Deliverables
- [ ] Pages dashboard complètes catalog/templates.
- [ ] Hooks/composants dédiés.
- [ ] Tests frontend minimum.

## Definition of done
- [ ] Code implemented
- [ ] Tests pass
- [ ] Docs updated if needed
- [ ] No architecture drift introduced
