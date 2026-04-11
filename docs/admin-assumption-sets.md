# Admin Assumption Sets

Calculation assumption sets are versioned configuration records used by the simplified annual engine. They must remain traceable because historical calculation snapshots may refer to the assumption set version or identifier that was active when the run was produced.

## Scopes

Supported scopes:

- `platform_default`: shared fallback assumptions.
- `country_default`: country-level defaults; `country_profile_id` is required.
- `organization_override`: assumptions owned by the current organization.

Only organization overrides carry `organization_id`. Platform and country defaults are visible to admins but are not tied to a tenant.

## JSON Validation

Admin writes validate these critical JSON sections explicitly:

- reference intensities for heating, cooling, DHW, lighting, ventilation and auxiliaries;
- economic defaults: discount rate, inflation rate and analysis period;
- BACS rules: score-to-class bounds for A, B, C and D;
- CO2 factors: non-empty source-to-factor mapping with non-negative numeric factors.

Invalid payloads are rejected before persistence.

## Recommended Workflow

1. List existing sets with `GET /api/v1/admin/assumption-sets`.
2. Inspect the current version with `GET /api/v1/admin/assumption-sets/{id}`.
3. For an unused draft set, edit it directly with `PATCH /api/v1/admin/assumption-sets/{id}`.
4. For a set already referenced by calculations, clone it with `POST /api/v1/admin/assumption-sets/{id}/clone`.
5. Update the cloned version and activate it with `POST /api/v1/admin/assumption-sets/{id}/activate`.
6. Deactivate obsolete versions only when they should no longer be selected for new calculations.

When a set has historical uses, the API marks it with:

- `is_locked: true`
- `historical_calculation_count`

Locked sets reject structural updates to assumptions, scope, version and name. This prevents silent drift in historical calculations while still allowing a clean new version through cloning.

## Endpoints

- `GET /api/v1/admin/assumption-sets`
- `GET /api/v1/admin/assumption-sets/{id}`
- `POST /api/v1/admin/assumption-sets`
- `PATCH /api/v1/admin/assumption-sets/{id}`
- `POST /api/v1/admin/assumption-sets/{id}/clone`
- `POST /api/v1/admin/assumption-sets/{id}/activate`
- `POST /api/v1/admin/assumption-sets/{id}/deactivate`
