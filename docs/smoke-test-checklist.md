# Smoke Test Checklist

Utiliser cette checklist avant une demonstration MVP+.

## Preparation

- [ ] Base de recette disponible.
- [ ] Migrations appliquees avec `alembic upgrade head`.
- [ ] Seeds charges avec `python scripts/seed_all.py`.
- [ ] Backend demarre.
- [ ] `GET /health` retourne `status=ok`.

## Login

- [ ] Connexion admin demo reussie.
- [ ] Token bearer present.
- [ ] `GET /api/v1/auth/me` retourne `demo@hotel-energy-audit.example.com`.

## Donnees Demo

- [ ] `DEMO-HOTEL-001` est disponible.
- [ ] `DEMO-HOTEL-SW-001` est disponible.
- [ ] `DEMO-RESIDENCE-001` est disponible.
- [ ] Chaque projet est en statut `ready`.
- [ ] Chaque projet contient batiment, zones, systemes, BACS et deux scenarios.

## Creation Projet

- [ ] Creation d'un projet manuel via `POST /api/v1/projects`.
- [ ] Lecture du projet cree via `GET /api/v1/projects/{project_id}`.
- [ ] Acces refuse ou 404 avec un utilisateur d'une autre organisation.

## Calcul

- [ ] Un projet complet retourne une readiness exploitable.
- [ ] `POST /api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate` retourne un resultat.
- [ ] `GET /api/v1/projects/{project_id}/scenarios/{scenario_id}/results/latest` retourne le meme run ou le plus recent.

## Comparaison

- [ ] Deux scenarios calcules peuvent etre compares.
- [ ] La reponse contient deux items.
- [ ] Un scenario recommande est present.

## Rapport Executif

- [ ] Generation executive via `/api/v1/reports/executive/{calculation_run_id}/generate`.
- [ ] Metadata rapport en statut `generated`.
- [ ] Telechargement PDF reussi.

## Rapport Detaille

- [ ] Generation detaillee via `/api/v1/reports/detailed/{calculation_run_id}/generate`.
- [ ] Metadata rapport en statut `generated`.
- [ ] Artefact distinct du rapport executif.
- [ ] Les options `include_assumptions`, `include_regulatory_section`, `include_annexes` sont testees au moins une fois en HTML.

## Administration Et Securite

- [ ] Un utilisateur non admin recoit `403` sur `/api/v1/admin/users`.
- [ ] Un rapport d'une autre organisation n'est pas telechargeable.
- [ ] Les logs audit sont consultables par admin via `/api/v1/admin/audit-logs`.

## Sortie De Recette

- [ ] Anomalies bloquantes listees.
- [ ] Anomalies non bloquantes qualifiees.
- [ ] Version de commit/branche notee.
- [ ] Date, testeur et environnement notes.
