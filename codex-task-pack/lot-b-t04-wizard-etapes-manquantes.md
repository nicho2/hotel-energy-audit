# Codex Task Template

## Metadata
- Task ID: LOT-B-T04
- Epic: Recalage MVP initial vs implémentation actuelle
- Feature: Wizard complet 10 étapes
- Priority: P0
- Owner: Frontend + Backend
- Status: todo
- Related files:
  - `frontend/features/wizard/**`
  - `frontend/features/*/components/*step*`
  - `frontend/features/wizard/api/*.ts`
  - `backend/app/api/v1/endpoints/wizard.py`
  - `backend/app/services/wizard_service.py`
  - `backend/tests/test_wizard_api.py`
- Dependencies:
  - LOT-A-T01
  - LOT-A-T02

## Context
Les specs 0/5 décrivent un wizard central en 10 étapes avec mode express/avancé.
Dans l’implémentation actuelle, seules certaines étapes ont un formulaire branché (`building`, `zones`, `systems`, `bacs`), et les autres restent en placeholder côté frontend avec validation simulée.
Cette tâche ferme cet écart fonctionnel cœur produit.

## Objective
Rendre toutes les étapes du wizard exploitables, sauvegardables et validables via API backend réelle.

## In scope
- Implémenter UI + schémas de validation pour étapes manquantes (`project`, `context`, `usage`, `solutions`, `scenarios`, `review`).
- Ajouter endpoints backend de save/validate par étape ou par domaine métier.
- Supprimer les placeholders dans `validate-step.ts` / `save-step.ts`.
- Assurer navigation wizard cohérente (next/previous, erreurs de validation).

## Out of scope
- Moteur de calcul détaillé (LOT-C).
- Optimisations UX avancées non MVP.

## Inputs / references
- `AGENTS.md`
- `docs/0-cahier-des-charges-initial.md`
- `docs/5-Specification-fonctionnelle-des-ecrans-et-du-wizard.md`
- `docs/7-Architecture-fonctionnelle-detaillee-des-API-backend.md`
- Additional docs:
  - `docs/8-contrats-json-detaille.md`

## Implementation notes
- Garder les pages et layouts fins; mettre la logique dans `features/*`.
- Utiliser React Hook Form + Zod alignés contrats backend.
- Standardiser les erreurs validation via `ApiResponse.errors`.
- Rebouclage par étape après livraison:
  1. Vérifier conformité de l’étape avec specs 5.
  2. Vérifier persistance réelle backend et reprise de session wizard.
  3. Ajuster wording/fields si mismatch avec docs 0-9.

## Acceptance criteria
- [ ] Les 10 étapes sont navigables et non placeholder.
- [ ] Chaque étape persistante dispose d’un save backend réel.
- [ ] La validation bloque le passage quand les données minimales sont absentes.
- [ ] Les contrats API et UI restent cohérents et versionnés.

## Tests to add or update
- [ ] Tests frontend (ou E2E) couvrant navigation et validation multi-étapes.
- [ ] Tests API wizard save/validate pour les nouvelles étapes.

## Deliverables
- [ ] UI wizard complète MVP.
- [ ] Endpoints backend associés.
- [ ] Tests intégration wizard.

## Definition of done
- [ ] Code implemented
- [ ] Tests pass
- [ ] Docs updated if needed
- [ ] No architecture drift introduced
