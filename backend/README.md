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

## Dev auth seed

```bash
py -3.12 scripts/seed_all.py
```

Utilisateur de dev cree ou mis a jour :

- email : `demo@hotel-energy-audit.example.com`
- mot de passe : `admin1234`
