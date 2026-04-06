# Hotel Energy Audit Starter

Starter repository for an accommodation-building energy audit web application.

## Purpose

This repository provides:

- a product and technical baseline for the MVP
- a Codex-ready execution framework
- a backend FastAPI skeleton
- a frontend Next.js skeleton
- structured docs for roadmap, backlog, architecture, APIs, and task execution

## Main folders

- `docs/` — product, MVP, backlog, architecture, API, task templates
- `backend/` — FastAPI starter
- `frontend/` — Next.js starter
- `AGENTS.md` — working rules for Codex / implementation agents

## Recommended first implementation order

1. Backend foundation
2. Auth + organizations
3. Projects + wizard shell
4. Building + zones + systems
5. BACS + scenarios + solutions
6. Calculation engine baseline
7. Results + comparison
8. Executive PDF reporting
9. Stabilization, tests, demo data

## Commands

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
alembic upgrade head
python scripts/seed_all.py
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Intended use with Codex

Use the repository together with:

- `AGENTS.md`
- `docs/mvp-plan.md`
- `docs/backlog.md`
- `docs/templates/codex-task-template.md`

Start each work item from a task file generated from the template.
