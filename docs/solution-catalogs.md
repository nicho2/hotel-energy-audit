# Solution Catalogs

The solution catalog is now persisted and administrable. Existing scenarios continue to store `solution_code`, so historical scenarios remain readable even if a solution is later deactivated.

## Data Model

Catalogs carry ownership and versioning metadata:

- `scope`: `global`, `country_specific`, or `organization_specific`
- `version`: stable catalog version label
- `country_code`: optional ISO-style country code for country-specific catalogs
- `organization_id`: present only for organization-specific catalogs
- `is_active`: controls whether active solution listings include the catalog

Solutions carry product and applicability metadata:

- `family`
- `target_scopes`
- `applicable_countries`
- `applicable_building_types`
- `applicable_zone_types`
- `bacs_impact_json`
- `lifetime_years`
- `default_quantity`, `default_unit`, `default_unit_cost`, `default_capex`
- `priority`
- `is_commercial_offer`
- `offer_reference`
- `is_active`

Seeded solution codes are stable identifiers. Do not rename them once scenarios can reference them.

## Catalog Scopes

Supported catalog scopes:

- `global`: platform-level reusable catalog.
- `country_specific`: catalog entries scoped to a country, for example `FR`.
- `organization_specific`: offers owned by an organization.

The frontend can list catalogs with:

`GET /api/v1/admin/solution-catalogs`

## Stable Filtering

Available solutions can be listed with:

`GET /api/v1/projects/solutions/catalog`

Supported filters:

- `country`
- `family`
- `building_type`
- `zone_type`
- `scope`
- `include_inactive`

Applicability rules are intentionally stable:

- an empty applicability list means "applies to all";
- a non-empty applicability list must contain the requested filter value;
- inactive catalogs and inactive solutions are hidden unless `include_inactive=true`;
- deactivated solutions remain available for historical scenario display but are rejected for new assignments.

The same filter set is available for admin users through:

`GET /api/v1/admin/solutions`

Admin listing defaults to `include_inactive=true` so back-office screens can show retired offers.

## Admin Workflow

1. List catalogs to find the target catalog.
2. Create organization-specific solutions in an `organization_specific` catalog.
3. Use clear stable `code` values because scenarios keep `solution_code` for traceability.
4. Deactivate obsolete offers instead of deleting them.
5. Use `include_inactive=true` for admin/history screens that need to explain older scenarios.

Admin endpoints:

- `GET /api/v1/admin/solution-catalogs`
- `GET /api/v1/admin/solutions`
- `POST /api/v1/admin/solutions`
- `PATCH /api/v1/admin/solutions/{solution_id}`
- `POST /api/v1/admin/solutions/{solution_id}/deactivate`

Commercial offer fields:

- `is_commercial_offer`
- `offer_reference`

When `is_commercial_offer=true`, `offer_reference` is required.

Recommended creation flow for organization offers:

1. Create or reuse an `organization_specific` catalog for the organization.
2. Create the solution with a unique `code`, `is_commercial_offer=true`, and an `offer_reference`.
3. Set applicability lists narrowly enough for frontend filtering.
4. Use deactivation for retirement; never delete a solution that may be referenced by scenarios.
