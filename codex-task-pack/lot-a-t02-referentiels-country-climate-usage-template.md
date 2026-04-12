# Codex Task Template

## Metadata
- Task ID: LOT-A-T02
- Epic: Recalage MVP initial vs implémentation actuelle
- Feature: Référentiels métier
- Priority: P0
- Owner: Backend
- Status: todo
- Related files:
  - `backend/app/db/models/`
  - `backend/app/repositories/`
  - `backend/app/services/`
  - `backend/app/api/v1/endpoints/`
  - `backend/app/schemas/`
  - `backend/migrations/versions/*`
  - `backend/scripts/seed_all.py`
- Dependencies:
  - LOT-A-T01 recommandé avant intégration complète projet

## Context
Les specs initiales 2/7/9 définissent des entités de référence (`CountryProfile`, `ClimateZone`, `UsageProfile`, `ProjectTemplate`).
L’implémentation actuelle ne possède pas ces modèles dans `backend/app/db/models`, ce qui bloque la conformité fonctionnelle du wizard, des templates et de la traçabilité des hypothèses.
Cette tâche crée le socle de données de référence et les APIs minimales pour les exploiter.

## Objective
Introduire les référentiels manquants avec persistence, services, endpoints et seed de base, pour rendre possible l’orchestration complète du flux projet/wizard.

## In scope
- Créer modèles SQLAlchemy + migrations pour `country_profiles`, `climate_zones`, `usage_profiles`, `project_templates`.
- Créer schémas Pydantic (read/create/update selon besoin MVP).
- Créer repositories + services métier dédiés.
- Exposer endpoints REST versionnés (au minimum lecture + CRUD templates).
- Ajouter données seed de base (au moins 1 pays, 2 climats, profils usage hôtellerie, 1 template exemple).

## Out of scope
- Moteur de calcul détaillé.
- UI complète des référentiels admin (peut être progressive).
- Localisation avancée multilingue des référentiels.

## Inputs / references
- `AGENTS.md`
- `docs/2-Modele-de-donnees-complet.md`
- `docs/5-Specification-fonctionnelle-des-ecrans-et-du-wizard.md`
- `docs/7-Architecture-fonctionnelle-detaillee-des-API-backend.md`
- `docs/9-structure-de-projet-FastAPI.md`
- Additional docs:
  - `docs/8-contrats-json-detaille.md`

## Implementation notes
- Respecter le découpage: endpoint mince, service métier, repository DB.
- Tous les endpoints doivent renvoyer `ApiResponse` (`data/meta/errors`).
- Prévoir clés fonctionnelles stables (`code`) pour pays/climat/profil usage.
- Rebouclage obligatoire après implémentation:
  1. Mapping complet entités docs 2 vs modèles réels.
  2. Vérifier que le wizard peut consommer ces données sans bricolage.
  3. Vérifier que les seeds permettent un démarrage immédiat du parcours MVP.

## Acceptance criteria
- [ ] Les 4 entités référentielles existent en DB avec migrations.
- [ ] APIs de lecture et CRUD templates sont opérationnelles.
- [ ] Les données seed rendent le flux projet exploitable sans saisie SQL manuelle.
- [ ] La structure backend reste conforme à l’architecture modulaire (doc 9).

## Tests to add or update
- [ ] Tests API référentiels (list/get, erreurs 404/validation).
- [ ] Tests `seed_all` assurant la présence de jeux de données minimaux.

## Deliverables
- [ ] Modèles + migrations + schémas + endpoints.
- [ ] Seeds référentiels.
- [ ] Tests backend associés.

## Definition of done
- [ ] Code implemented
- [ ] Tests pass
- [ ] Docs updated if needed
- [ ] No architecture drift introduced
