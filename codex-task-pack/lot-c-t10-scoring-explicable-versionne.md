# Codex Task Template

## Metadata
- Task ID: LOT-C-T10
- Epic: Recalage MVP initial vs implémentation actuelle
- Feature: Scoring comparateur explicable
- Priority: P1
- Owner: Backend Results
- Status: todo
- Related files:
  - `backend/app/services/results_service.py`
  - `backend/app/schemas/scenario_comparison.py`
  - `backend/app/services/assumption_set_service.py`
  - `backend/tests/test_scenarios_compare_api.py`
- Dependencies:
  - LOT-C-T09

## Context
Les specs et garde-fous AGENTS imposent d’éviter les scores “magic” non traçables.
Le comparateur actuel calcule un score avec pondérations hardcodées.
Cette tâche vise la transparence, la version et l’explicabilité commerciale.

## Objective
Rendre le scoring de recommandation versionné, paramétrable et explicable dans l’API.

## In scope
- Externaliser pondérations/règles de score dans assumptions versionnées.
- Refactorer le calcul de score dans un module dédié.
- Retourner le détail de contribution des sous-scores (énergie, BACS, ROI, CAPEX).
- Mettre à jour message de recommandation à partir des contributions dominantes.

## Out of scope
- IA de recommandation avancée.
- Personnalisation score par utilisateur final.

## Inputs / references
- `AGENTS.md`
- `docs/0-cahier-des-charges-initial.md`
- `docs/3-Moteur-de-calcul-simplifie.md`
- `docs/8-contrats-json-detaille.md`
- Additional docs:
  - `docs/backlog.md`

## Implementation notes
- Conserver rétrocompatibilité du champ `score` existant.
- Ajouter nouveaux champs explicatifs sans casser clients existants.
- Rebouclage:
  1. Vérifier absence de constantes arbitraires non documentées.
  2. Vérifier que le score est reproductible via assumption set + snapshot.
  3. Vérifier que la recommandation API est justifiable métier.

## Acceptance criteria
- [ ] Pondérations de score non hardcodées dans le service principal.
- [ ] Réponse compare inclut détails de scoring explicables.
- [ ] Tests valident stabilité et reproductibilité du score.

## Tests to add or update
- [ ] `test_scenarios_compare_api.py` avec vérification de score breakdown.
- [ ] Tests unitaires du module de scoring.

## Deliverables
- [ ] Module scoring versionné.
- [ ] API comparaison enrichie.
- [ ] Tests et documentation de calcul du score.

## Definition of done
- [ ] Code implemented
- [ ] Tests pass
- [ ] Docs updated if needed
- [ ] No architecture drift introduced
