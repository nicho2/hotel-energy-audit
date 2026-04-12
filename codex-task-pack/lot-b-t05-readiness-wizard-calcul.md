# Codex Task Template

## Metadata
- Task ID: LOT-B-T05
- Epic: Recalage MVP initial vs implémentation actuelle
- Feature: Readiness wizard & calcul
- Priority: P0
- Owner: Backend
- Status: todo
- Related files:
  - `backend/app/services/wizard_service.py`
  - `backend/app/services/readiness_service.py`
  - `backend/app/schemas/wizard.py`
  - `backend/app/schemas/readiness.py`
  - `backend/tests/test_wizard_api.py`
  - `backend/tests/test_calculation_readiness_api.py`
- Dependencies:
  - LOT-B-T04 recommandé

## Context
L’état readiness actuel est incohérent: blocage quasi permanent côté wizard et warning obsolète sur scénarios implicites.
Les specs 0/5/7 imposent un enchaînement clair vers le calcul, fondé sur validations réelles.
Cette tâche rétablit la logique de préparation au calcul et sa lisibilité.

## Objective
Produire une readiness fiable, explicable et actionnable, côté wizard et côté calcul.

## In scope
- Revoir règles de blocage par étape et statut global (`ready/not_ready`).
- Remplacer messages obsolètes et incohérents.
- Unifier les contrôles entre `WizardService` et `ReadinessService`.
- Exposer raisons de blocage/warnings structurées et consommables front.

## Out of scope
- Implémentation du moteur de calcul détaillé.
- Refonte UX globale du wizard.

## Inputs / references
- `AGENTS.md`
- `docs/3-Moteur-de-calcul-simplifie.md`
- `docs/5-Specification-fonctionnelle-des-ecrans-et-du-wizard.md`
- `docs/7-Architecture-fonctionnelle-detaillee-des-API-backend.md`
- Additional docs:
  - `docs/8-contrats-json-detaille.md`

## Implementation notes
- Éviter tout hardcode contradictoire avec l’état réel des données.
- Définir une matrice explicite “donnée manquante -> blocage/warning”.
- Rebouclage systématique:
  1. Vérifier conformité des règles avec prérequis calcul docs 3/5.
  2. Tester cas limites (aucun système, zones invalides, projet incomplet).
  3. Ajuster niveaux de sévérité jusqu’à cohérence métier.

## Acceptance criteria
- [ ] `status=ready` possible quand les prérequis réels sont satisfaits.
- [ ] Les warnings/erreurs sont pertinents et non obsolètes.
- [ ] Les endpoints readiness/wizard donnent des informations cohérentes entre eux.

## Tests to add or update
- [ ] `test_wizard_api.py` pour transitions d’étapes et blocking steps.
- [ ] `test_calculation_readiness_api.py` pour cas ready/not_ready et messages.

## Deliverables
- [ ] Services readiness/wizard alignés.
- [ ] Schémas/réponses stabilisés.
- [ ] Tests couvrant les scénarios clés.

## Definition of done
- [ ] Code implemented
- [ ] Tests pass
- [ ] Docs updated if needed
- [ ] No architecture drift introduced
