# Codex Task Template

## Metadata
- Task ID: LOT-C-T08
- Epic: Recalage MVP initial vs implémentation actuelle
- Feature: Impacts scénarios (solutions + BACS)
- Priority: P0
- Owner: Backend Calculation + Scenarios
- Status: todo
- Related files:
  - `backend/app/services/calculation_service.py`
  - `backend/app/services/scenario_service.py`
  - `backend/app/repositories/scenario_solution_repository.py`
  - `backend/app/calculation/engine.py`
  - `backend/tests/test_scenarios_management_api.py`
  - `backend/tests/test_calculations_api.py`
- Dependencies:
  - LOT-C-T07

## Context
Les scénarios et solutions existent côté CRUD, mais l’entrée de calcul n’embarque pas réellement les solutions sélectionnées (`selected_solutions=[]`).
Les gains BACS et techniques ne sont donc pas réellement simulés dans les résultats.
Les specs 0/3/4 exigent une comparaison de bouquets de solutions crédible.

## Objective
Intégrer les solutions et fonctions BACS dans la chaîne de calcul pour générer des écarts avant/après réellement fondés sur le scénario.

## In scope
- Charger les assignments de scénario au moment du calcul.
- Appliquer impacts des solutions selon scope (global/zone/system) et règles de cumul.
- Appliquer impacts BACS présents/cibles dans la même chaîne.
- Tracer les impacts appliqués (auditabilité).

## Out of scope
- Optimisation combinatoire avancée multi-bouquets.
- Moteur de dépendances complexes de catalogue v2.

## Inputs / references
- `AGENTS.md`
- `docs/0-cahier-des-charges-initial.md`
- `docs/3-Moteur-de-calcul-simplifie.md`
- `docs/4-Specification-de-calcul-detaillee.md`
- Additional docs:
  - `docs/solution-catalogs.md`

## Implementation notes
- Définir un ordre stable d’application des impacts pour éviter les incohérences.
- Injecter dans snapshot la liste des solutions effectivement prises en compte.
- Rebouclage obligatoire:
  1. Vérifier qu’un scénario sans solution = baseline inchangée.
  2. Vérifier qu’un scénario avec solution produit variation explicable.
  3. Vérifier cohérence avec classes BACS calculées.

## Acceptance criteria
- [ ] `selected_solutions` est alimenté depuis la DB scénario.
- [ ] Les résultats changent en fonction des solutions/BACS du scénario.
- [ ] Les impacts sont traçables dans `input_snapshot/messages`.

## Tests to add or update
- [ ] Tests API calcul comparant 2 scénarios (avec/sans solutions).
- [ ] Tests unitaires règles de cumul d’impacts.

## Deliverables
- [ ] Pipeline calcul branché aux scénarios.
- [ ] Règles d’impact documentées dans le code.
- [ ] Tests de non-régression.

## Definition of done
- [ ] Code implemented
- [ ] Tests pass
- [ ] Docs updated if needed
- [ ] No architecture drift introduced
