# Codex Task Template

## Metadata
- Task ID: LOT-C-T09
- Epic: Recalage MVP initial vs implémentation actuelle
- Feature: ROI et économique multi-indicateurs
- Priority: P0
- Owner: Backend Calculation
- Status: todo
- Related files:
  - `backend/app/calculation/engine.py`
  - `backend/app/services/results_service.py`
  - `backend/app/db/models/economic_result.py`
  - `backend/app/schemas/calculations.py`
  - `backend/tests/test_results_api.py`
- Dependencies:
  - LOT-C-T07
  - LOT-C-T08

## Context
Le besoin initial demande CAPEX/OPEX/économies/payback/VAN/TRI/cash-flow simplifié.
L’implémentation actuelle couvre partiellement ces éléments et reste proche d’un placeholder.
Pour un usage commercial/exploitant, le volet économique doit être robuste et traçable.

## Objective
Compléter le moteur économique et exposer des indicateurs ROI cohérents avec les hypothèses versionnées.

## In scope
- Modéliser OPEX baseline/scénario + économies annuelles.
- Calculer payback simple, VAN, TRI, cash-flow simplifié.
- Utiliser hypothèses économiques (prix énergie, inflation, discount rate, période, maintenance, subventions).
- Exposer les valeurs dans API résultats/comparateur/rapport.

## Out of scope
- Modèles financiers complexes (fiscalité avancée, Monte Carlo).
- Intégration ERP/comptable.

## Inputs / references
- `AGENTS.md`
- `docs/0-cahier-des-charges-initial.md`
- `docs/3-Moteur-de-calcul-simplifie.md`
- `docs/4-Specification-de-calcul-detaillee.md`
- Additional docs:
  - `docs/6-Specification-du-rapport-PDF.md`

## Implementation notes
- Garder une approche lisible/expliquable, orientée décision.
- Ajouter gestion des cas limites (capex=0, économies négatives, TRI non défini).
- Rebouclage:
  1. Vérifier alignement des indicateurs avec specs 0/3/4.
  2. Vérifier cohérence entre APIs résultats, compare et rapport.
  3. Ajuster schémas si information économique manquante.

## Acceptance criteria
- [ ] Tous les indicateurs économiques MVP sont calculés ou explicitement “non calculable”.
- [ ] Les hypothèses économiques utilisées sont traçables.
- [ ] Les endpoints résultats/comparateur exposent des valeurs cohérentes.

## Tests to add or update
- [ ] Tests unitaires VAN/TRI/payback/cash-flow.
- [ ] Tests API résultats/comparaison avec cas nominaux et cas limites.

## Deliverables
- [ ] Moteur économique complété.
- [ ] Schémas/API enrichis.
- [ ] Jeu de tests robuste.

## Definition of done
- [ ] Code implemented
- [ ] Tests pass
- [ ] Docs updated if needed
- [ ] No architecture drift introduced
