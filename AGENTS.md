# AGENTS.md

## Mission

Build an MVP for a web application that estimates energy performance and improvement scenarios for existing accommodation buildings such as hotels, apart-hotels, and residences.

The application must remain:

- simple to use
- commercially usable
- technically credible
- traceable in its assumptions
- designed for comparison of scenarios, not for full regulatory simulation

## Product guardrails

1. The V1 engine is a **simplified annual estimation engine**.
2. Do not drift into full dynamic simulation or full regulatory compliance tooling.
3. The application is optimized for:
   - exploitants
   - commerciaux
   - pre-audit / pre-sales / decision support
4. The strongest differentiators are:
   - zoning by function and orientation
   - room automation logic
   - BACS scoring and target improvement
   - scenario comparison
   - executive-grade PDF reporting

## Technical guardrails

- Backend: FastAPI + SQLAlchemy 2 + Pydantic 2 + PostgreSQL
- Frontend: Next.js + TypeScript + TanStack Query + React Hook Form + Zod
- Architecture: modular monolith
- Reporting: HTML templates rendered to PDF
- All APIs must follow the standardized `data / meta / errors` structure.
- Every calculation must be reproducible through snapshots and versioned assumptions.

## Mandatory working method

For each non-trivial implementation task:

1. Read the relevant docs in `docs/`
2. Restate the exact scope
3. Identify dependencies
4. Implement the smallest coherent slice
5. Add or update tests
6. Update documentation if behavior changed
7. Keep changes local to the relevant feature/module

## File-level guidance

### Backend
- Keep routes thin
- Put business logic in services
- Put DB access in repositories
- Keep calculation logic inside `app/calculation/`
- Do not query the DB from inside the calculation engine
- Do not generate PDFs from API routes directly

### Frontend
- Keep pages thin
- Put feature logic inside `features/*`
- Use server state via TanStack Query
- Use Zod schemas aligned with backend contracts
- Keep express mode as default UX
- Avoid global state unless truly necessary

## Quality requirements

A task is not done unless:

- code builds / runs
- tests added or updated when relevant
- lint/format pass
- no obvious architectural drift
- docs remain coherent with the implementation

## Priorities when trade-offs appear

1. correctness of domain behavior
2. consistency with architecture
3. clarity and maintainability
4. polish

## What to avoid

- premature microservices
- hidden business logic in UI
- unversioned coefficients or assumptions
- equal-weight "magic" scoring without traceability
- vague TODO-driven implementation without acceptance criteria

## Reference docs to consult first

- `docs/final-spec.md`
- `docs/mvp-plan.md`
- `docs/backlog.md`
- `docs/architecture-overview.md`
- `docs/api-contracts.md`
- `docs/templates/codex-task-template.md`
