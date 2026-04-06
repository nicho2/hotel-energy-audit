# Final Consolidated Specification

## Product summary

Build a web application for simplified energy audit and scenario comparison for **existing accommodation buildings**:
- hotels
- apart-hotels
- accommodation residences

The product is aimed primarily at:
- exploitants
- commerciaux
- pre-sales and pre-audit use

The application must remain simple, professional, explainable, and useful for decision support.

## Core principles
- simplified annual estimation engine
- zoning by function and orientation
- BACS assessment and improvement logic
- scenario comparison
- ROI and CO2 outputs
- executive PDF reporting

## Main modules
1. auth and organizations
2. projects and templates
3. wizard
4. building / zones / usage / systems
5. BACS
6. solutions and scenarios
7. calculation engine
8. results and comparison
9. reporting
10. admin configuration
11. audit and demo data

## Calculation model
The V1 engine is annual and simplified:
- baseline by usage
- correction coefficients by climate, envelope, compacity, occupation, zoning, orientation, and systems
- BACS functions applied by usage/zone
- solutions combined sequentially on residual energy
- economics with CAPEX, annual savings, payback, NPV, IRR
- CO2 from energy source factors

## UX
- express mode first
- advanced mode section by section
- wizard with 10 steps
- commercial-oriented result presentation
- transparent assumptions page

## Technical stack
### Backend
- FastAPI
- SQLAlchemy 2
- Pydantic 2
- PostgreSQL
- Alembic

### Frontend
- Next.js
- TypeScript
- TanStack Query
- React Hook Form
- Zod

### Reporting
- HTML templates
- PDF generation

## API conventions
- `/api/v1`
- REST JSON
- `data / meta / errors`
- UUID identifiers
- ISO date format
- ratios sent as decimal values (e.g. 0.12)

## MVP
The MVP must support a complete user path from project creation to executive PDF generation on hotel demo cases.

See:
- `docs/mvp-plan.md`
- `docs/backlog.md`
- `docs/architecture-overview.md`
- `docs/api-contracts.md`
