# Backend

Socle backend FastAPI du MVP `hotel-energy-audit`.

## Prerequisites

- Python 3.12+
- PostgreSQL 15+ pour les prochaines taches de persistence

## Installation

```bash
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
Copy-Item .env.example .env
```

## Run

```bash
uvicorn app.main:app --reload
```

L'API expose:

- `GET /health`
- base path versionnee `GET /api/v1/...` pour les routeurs principaux encore vides

En developpement, l'origine frontend Next.js est autorisee via `CORS_ALLOWED_ORIGINS`.
La valeur par defaut couvre `http://localhost:3000` et `http://127.0.0.1:3000`.

## Test

```bash
py -3.12 -m pytest
```

Commande ciblee P0 backend :

```bash
py -3.12 -m pytest tests/test_auth_api.py tests/test_projects_api.py tests/test_buildings_api.py tests/test_zones_api.py tests/test_bacs_api.py tests/test_calculations_api.py tests/test_results_api.py tests/test_scenarios_compare_api.py tests/test_reports_api.py tests/test_calculation_engine.py tests/test_project_service.py tests/test_readiness_service.py
```

## Migrations

```bash
alembic upgrade head
```

Par defaut, l'exemple de configuration cible un PostgreSQL local sur `localhost:5432`
avec l'utilisateur `postgres`, le mot de passe `admin` et la base `hotel_audit`.

## Demo seed

```bash
py -3.12 scripts/seed_all.py
```

Le script charge en une seule commande :

- l'organisation de demonstration principale
- les comptes demo admin, commercial et partenaire
- 3 projets demonstration prets a visualiser
- des donnees batiment, zones, systemes, BACS, scenarios et resultats persistants

Comptes disponibles :

- admin : `demo@hotel-energy-audit.example.com` / `admin1234`
- commercial : `sales@hotel-energy-audit.example.com` / `sales1234`
- partenaire : `partner@hotel-energy-audit.example.com` / `partner1234`

Cas de demonstration charges :

- `DEMO-HOTEL-001` : Hotel Lumiere Paris
- `DEMO-APARTHOTEL-001` : Canal Suites Aparthotel
- `DEMO-RESIDENCE-001` : Residence Azur Seaside
