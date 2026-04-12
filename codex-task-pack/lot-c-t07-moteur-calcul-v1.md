# Codex Task Template

## Metadata
- Task ID: LOT-C-T07
- Epic: Recalage MVP initial vs implémentation actuelle
- Feature: Moteur de calcul énergétique simplifié V1
- Priority: P0
- Owner: Backend Calculation
- Status: todo
- Related files:
  - `backend/app/calculation/engine.py`
  - `backend/app/calculation/types.py`
  - `backend/app/services/calculation_service.py`
  - `backend/app/services/assumption_set_service.py`
  - `backend/tests/test_calculation_engine.py`
  - `backend/tests/test_calculations_api.py`
- Dependencies:
  - LOT-A-T01
  - LOT-A-T02

## Context
Le moteur actuel renvoie des valeurs statiques (`placeholder-v1`) et ne respecte pas les formules et facteurs définis dans les docs 3 et 4.
Le produit cible est un moteur d’estimation annuelle simplifiée, traçable, orienté comparaison de scénarios.
Cette tâche est la plus critique pour la crédibilité métier.

## Objective
Implémenter un moteur V1 semi-physique simplifié, piloté par hypothèses versionnées, couvrant usages énergétiques et consolidation.

## In scope
- Baseline par usage: chauffage, refroidissement, ventilation, ECS, éclairage, auxiliaires.
- Application des facteurs (climat, construction, compacité, occupation, enveloppe/infiltration, systèmes, orientation/zone, BACS).
- Consolidation sorties: total, par usage, par zone, indicateurs de gain.
- Versionnage du moteur + snapshot d’entrée exploitable.

## Out of scope
- Simulation thermique dynamique horaire.
- Conformité réglementaire complète.

## Inputs / references
- `AGENTS.md`
- `docs/3-Moteur-de-calcul-simplifie.md`
- `docs/4-Specification-de-calcul-detaillee.md`
- `docs/0-cahier-des-charges-initial.md`
- Additional docs:
  - `docs/api-contracts.md`

## Implementation notes
- Décomposer le moteur en sous-fonctions testables (baseline/facteurs/consolidation).
- Zéro accès DB depuis `app/calculation/` (les données arrivent via service).
- Documenter les hypothèses appliquées dans `messages/warnings`.
- Rebouclage strict:
  1. Vérifier mapping des variables d’entrée docs 4 -> `CalculationInput`.
  2. Vérifier plausibilité des ordres de grandeur et écarts relatifs.
  3. Vérifier reproductibilité snapshot/version moteur.

## Acceptance criteria
- [ ] Le moteur ne dépend plus de constantes placeholder fixes.
- [ ] Les sorties varient effectivement selon les entrées projet/zones/systèmes/BACS.
- [ ] Le snapshot contient les hypothèses nécessaires à la reproductibilité.
- [ ] Les tests valident au moins un cas de variation significative par facteur.

## Tests to add or update
- [ ] Tests unitaires calcul par usage + facteurs.
- [ ] Tests API calcul confirmant la variation des résultats selon inputs.

## Deliverables
- [ ] Nouveau moteur V1 opérationnel.
- [ ] Contrats de sortie maintenus ou migrés proprement.
- [ ] Couverture de tests renforcée.

## Definition of done
- [ ] Code implemented
- [ ] Tests pass
- [ ] Docs updated if needed
- [ ] No architecture drift introduced
