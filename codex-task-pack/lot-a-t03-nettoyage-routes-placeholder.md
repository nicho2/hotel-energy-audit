# Codex Task Template

## Metadata
- Task ID: LOT-A-T03
- Epic: Recalage MVP initial vs implémentation actuelle
- Feature: Hygiène architecture API
- Priority: P2
- Owner: Backend
- Status: todo
- Related files:
  - `backend/app/api/v1/*.py`
  - `backend/app/api/v1/endpoints/*.py`
  - `backend/app/api/v1/router.py`
  - `backend/tests/`
- Dependencies:
  - Aucune

## Context
Le projet contient des modules API legacy avec endpoints `__placeholder__` en parallèle des endpoints actifs sous `app/api/v1/endpoints`.
Même s’ils ne sont pas tous branchés, cette duplication crée du bruit, de l’ambiguïté et une perception de non-finition.
Les specs 7/9 demandent une API structurée et lisible.

## Objective
Supprimer les artefacts API placeholder et conserver un seul chemin clair d’exposition des endpoints.

## In scope
- Inventorier tous les endpoints placeholder/legacy.
- Supprimer ou déplacer en espace explicitement non exécuté (`legacy/`).
- Vérifier que `router.py` n’inclut que les routeurs officiels.
- Ajuster tests/documentation si chemins ont changé.

## Out of scope
- Refonte fonctionnelle des endpoints métier.
- Changement de contrat JSON.

## Inputs / references
- `AGENTS.md`
- `docs/7-Architecture-fonctionnelle-detaillee-des-API-backend.md`
- `docs/9-structure-de-projet-FastAPI.md`
- Additional docs:
  - `docs/api-contracts.md`

## Implementation notes
- Ne pas casser la rétrocompatibilité des routes utilisées par le frontend.
- Garder l’arborescence `endpoints/` comme source unique.
- Rebouclage demandé:
  1. Relire docs 7/9 et vérifier la clarté finale des domaines API.
  2. Vérifier qu’aucun test ne dépend encore de routes placeholder.
  3. Vérifier qu’OpenAPI expose uniquement les routes métier.

## Acceptance criteria
- [ ] Aucun endpoint `__placeholder__` accessible dans l’API active.
- [ ] Le routeur principal reste fonctionnel et cohérent.
- [ ] L’architecture API est simplifiée et non ambiguë.

## Tests to add or update
- [ ] Smoke test OpenAPI pour valider la liste des routes exposées.
- [ ] Mise à jour tests impactés par suppression legacy.

## Deliverables
- [ ] Nettoyage modules placeholder.
- [ ] Router API consolidé.
- [ ] Tests/smoke API mis à jour.

## Definition of done
- [ ] Code implemented
- [ ] Tests pass
- [ ] Docs updated if needed
- [ ] No architecture drift introduced
