# Backend

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
alembic upgrade head
python scripts/seed_all.py
uvicorn app.main:app --reload
```
