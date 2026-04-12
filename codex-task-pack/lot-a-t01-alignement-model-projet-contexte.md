# Codex Task Template

## Metadata
- Task ID: LOT-A-T01
- Epic: Recalage MVP initial vs implémentation actuelle
- Feature: Projets / Contexte pays-climat
- Priority: P0
- Owner: Backend
- Status: todo
- Related files:
  - `backend/app/db/models/project.py`
  - `backend/app/schemas/projects.py`
  - `backend/app/services/project_service.py`
  - `backend/app/repositories/project_repository.py`
  - `backend/migrations/versions/*`
  - `backend/tests/test_projects_api.py`
- Dependencies:
  - Aucune dépendance bloquante

## Context
Les specs initiales (docs 0, 2, 5, 7, 8) imposent que le projet porte explicitement le contexte pays et climat.
Aujourd’hui, `ProjectCreate` accepte `country_profile_id` et `climate_zone_id`, mais ces champs ne sont pas persistés dans `Project` et n’apparaissent pas dans `ProjectResponse`.
Cela crée un écart fonctionnel (wizard contexte incomplet) et un risque de non-reproductibilité des calculs.
Cette tâche remet à niveau la persistance et le contrat API du module projet.

## Objective
Rendre `country_profile_id` et `climate_zone_id` pleinement supportés de bout en bout (DB, service, API, tests), en cohérence avec le besoin initial de contexte pays/climat.

## In scope
- Ajouter les colonnes `country_profile_id` et `climate_zone_id` au modèle `projects`.
- Exposer les champs dans `ProjectResponse` et les retours list/get/create/update.
- Mettre à jour repository/service pour lecture/écriture robuste.
- Ajouter/adapter tests API projet couvrant création, lecture, mise à jour et isolation org.

## Out of scope
- Création complète des tables `country_profiles` et `climate_zones` (traitée en LOT-A-T02).
- Refonte UX wizard contexte.
- Changement de logique de calcul.

## Inputs / references
- `AGENTS.md`
- `docs/0-cahier-des-charges-initial.md`
- `docs/2-Modele-de-donnees-complet.md`
- `docs/5-Specification-fonctionnelle-des-ecrans-et-du-wizard.md`
- `docs/7-Architecture-fonctionnelle-detaillee-des-API-backend.md`
- `docs/8-contrats-json-detaille.md`
- Additional docs:
  - `docs/9-structure-de-projet-FastAPI.md`

## Implementation notes
- Migration Alembic idempotente, avec nullable temporaire si nécessaire pour compat data existante.
- Ajouter validation métier minimale: `country_profile_id` et `climate_zone_id` doivent être fournis à la création en mode strict MVP (ou documenter le fallback).
- Conserver le format API `data/meta/errors` sans régression.
- Rebouclage obligatoire avant merge:
  1. Vérifier conformité avec docs 0/2/7/8 (présence champs + contrat API).
  2. Vérifier absence de rupture sur endpoints existants (`/api/v1/projects`).
  3. Ajuster migration/schémas/tests jusqu’à alignement complet.

## Acceptance criteria
- [ ] `projects` persiste `country_profile_id` et `climate_zone_id`.
- [ ] `ProjectResponse` contient les deux champs et les endpoints les renvoient.
- [ ] Les tests API projet confirment le round-trip complet des champs.
- [ ] Le comportement respecte les specs 0-9 sur le contexte pays/climat.

## Tests to add or update
- [ ] `backend/tests/test_projects_api.py` (create/list/get/update avec country/climate).
- [ ] Test migration (ou test metadata) vérifiant les nouvelles colonnes.

## Deliverables
- [ ] Migration DB + modèle SQLAlchemy mis à jour.
- [ ] Schémas/service/repository projet alignés.
- [ ] Suite de tests projet mise à jour.

## Definition of done
- [ ] Code implemented
- [ ] Tests pass
- [ ] Docs updated if needed
- [ ] No architecture drift introduced
