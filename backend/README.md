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

## Test

```bash
pytest
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
