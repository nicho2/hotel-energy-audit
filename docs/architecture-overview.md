# Architecture Overview

## System view

- Frontend Next.js
- Backend FastAPI
- PostgreSQL
- File storage for PDF artifacts
- Calculation engine
- Reporting engine

## Backend modules

- auth
- users
- organizations
- branding
- projects
- wizard
- building
- zones
- usage
- systems
- bacs
- solutions
- scenarios
- calculations
- results
- reports
- admin
- audit

## Backend architecture style

Modular monolith with clear layers:
- API
- Schemas
- Services
- Repositories
- Domain engines
- Persistence

## Frontend architecture style

Feature-oriented with:
- app router pages
- feature modules
- shared UI components
- centralized API client
- provider layer for auth and server state

## Calculation engine sub-modules
- baseline
- BACS scoring
- solution impact
- economics
- consolidation
- snapshots

## Reporting pipeline
- report builder
- context serializer
- HTML renderer
- PDF generator
- artifact storage
