# MVP Plan

## Goal

Deliver an MVP that allows a user to:

1. create a project
2. complete a wizard for an existing accommodation building
3. define functional zones and orientations
4. describe main technical systems
5. evaluate the current BACS level
6. create scenarios with solution bouquets
7. calculate estimated energy, CO2, BACS, and ROI results
8. compare scenarios
9. generate an executive PDF report

## MVP scope

### Included
- organizations and users
- projects and templates
- wizard (express-first)
- building, zones, usage, systems
- BACS questionnaire and scoring
- solution catalog
- scenarios and scenario duplication
- readiness checks
- simplified annual calculation engine
- scenario comparison
- executive PDF report
- FR/EN support
- minimal branding
- audit/history minimal
- demo data

### Deferred
- Excel import
- GTB live connectors
- SSO
- multi-building projects
- advanced PDF template editor
- full detailed report builder if schedule is tight
- full country-by-country regulatory depth

## Delivery lots

### Lot 1 — Foundation
- backend bootstrap
- frontend bootstrap
- DB setup
- error model
- logging
- tooling

### Lot 2 — Auth and organization
- auth
- RBAC
- organization isolation
- branding basics

### Lot 3 — Projects and wizard shell
- project CRUD
- project overview
- wizard progress
- first steps

### Lot 4 — Building model
- building
- zones
- usage profiles
- systems

### Lot 5 — BACS and scenarios
- BACS questionnaire
- BACS scoring
- solution catalog
- scenarios

### Lot 6 — Calculation
- baseline
- BACS impact
- solution impact
- economics
- messages
- snapshots

### Lot 7 — Results and report
- results API
- comparison
- executive PDF

### Lot 8 — Stabilization
- tests
- demo data
- audit/history
- hardening

## Acceptance criteria for MVP

The MVP is considered successful when a user can complete the full path on a hotel demo case, without developer intervention, and obtain a professional PDF report from valid scenario calculations.
