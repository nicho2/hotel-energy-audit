# API Contracts Overview

## Response envelope

```json
{
  "data": {},
  "meta": {},
  "errors": []
}
```

## Error format

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Validation failed",
  "field": "gross_floor_area_m2",
  "details": {
    "reason": "must be greater than zero"
  }
}
```

## Main endpoint groups
- `/api/v1/auth`
- `/api/v1/admin/users`
- `/api/v1/admin/users/{id}/deactivate`
- `/api/v1/admin/assumption-sets`
- `/api/v1/admin/assumption-sets/{id}`
- `/api/v1/admin/assumption-sets/{id}/clone`
- `/api/v1/admin/assumption-sets/{id}/activate`
- `/api/v1/admin/assumption-sets/{id}/deactivate`
- `/api/v1/admin/branding`
- `/api/v1/admin/branding/{id}`
- `/api/v1/admin/audit-logs`
- `/api/v1/admin/solution-catalogs`
- `/api/v1/admin/solutions`
- `/api/v1/admin/solutions/{id}`
- `/api/v1/admin/solutions/{id}/deactivate`
- `/api/v1/branding`
- `/api/v1/projects`
- `/api/v1/projects/{id}/assumptions`
- `/api/v1/projects/{id}/history`
- `/api/v1/projects/{id}/scenarios/{scenarioId}/history`
- `/api/v1/projects/{id}/wizard`
- `/api/v1/projects/{id}/building`
- `/api/v1/projects/{id}/zones`
- `/api/v1/projects/{id}/systems`
- `/api/v1/projects/{id}/bacs`
- `/api/v1/projects/solutions/catalog`
- `/api/v1/projects/{id}/scenarios`
- `/api/v1/projects/{id}/scenarios/compare`
- `/api/v1/projects/{id}/scenarios/{scenarioId}/calculate`
- `/api/v1/projects/{id}/scenarios/{scenarioId}/results/latest`
- `/api/v1/projects/{id}/scenarios/{scenarioId}/results/by-use`
- `/api/v1/projects/{id}/scenarios/{scenarioId}/results/by-zone`
- `/api/v1/calculations/{id}`
- `/api/v1/reports`
- `/api/v1/reports/executive/{calculationRunId}/html`
- `/api/v1/reports/executive/{calculationRunId}/generate`
- `/api/v1/reports/detailed/{calculationRunId}/html`
- `/api/v1/reports/detailed/{calculationRunId}/generate`
- `/api/v1/reports/{reportId}`
- `/api/v1/reports/{reportId}/download`

Generated report metadata now retains the optional `branding_profile_id` used during rendering.
Detailed generation also supports `include_assumptions`, `include_regulatory_section`, and `include_annexes`.

## Main enums
### auth token claims
- `sub`
- `organization_id`
- `email`
- `role`
- `type`
- `iat`
- `exp`

### user roles
- `org_admin`
- `org_member`
- `member`

### branding profile fields
- `id`
- `organization_id`
- `name`
- `company_name`
- `accent_color`
- `logo_text`
- `contact_email`
- `cover_tagline`
- `footer_note`
- `is_default`

### project history event fields
- `action`
- `actor`
- `occurred_at`
- `summary`

### project_history_action
- project_created
- project_updated
- project_archived
- scenario_created
- scenario_updated
- scenario_deleted
- scenario_calculated
- report_generated
- assumption_set_updated
- solution_created
- solution_updated
- solution_deactivated

### audit log fields
- `id`
- `entity_type`
- `entity_id`
- `action`
- `before_json`
- `after_json`
- `user_id`
- `organization_id`
- `project_id`
- `scenario_id`
- `timestamp`

### audit log filters
- `entity_type`
- `entity_id`
- `action`
- `project_id`
- `scenario_id`
- `user_id`
- `date_from`
- `date_to`
- `limit`

### project assumptions fields
- `project_id`
- `calculation_run_id`
- `scenario_name`
- `engine_version`
- `generated_at`
- `warnings`
- `sections[].key`
- `sections[].title`
- `sections[].items[].key`
- `sections[].items[].label`
- `sections[].items[].value`
- `sections[].items[].source`
- `sections[].items[].note`
- `sections[].items[].warning`

### calculation assumption set fields
- `id`
- `organization_id`
- `country_profile_id`
- `cloned_from_id`
- `name`
- `version`
- `scope`
- `heating_model_json`
- `cooling_model_json`
- `ventilation_model_json`
- `dhw_model_json`
- `lighting_model_json`
- `auxiliaries_model_json`
- `economic_defaults_json`
- `bacs_rules_json`
- `scoring_rules_json`
- `co2_factors_json`
- `notes`
- `is_active`
- `is_locked`
- `historical_calculation_count`
- `created_at`
- `updated_at`

### calculation_assumption_set_scope
- platform_default
- country_default
- organization_override

### solution catalog fields
- `id`
- `organization_id`
- `name`
- `version`
- `scope`
- `country_code`
- `is_active`
- `created_at`
- `updated_at`

### calculation engine V1 snapshot
- `engine_version`: `simplified-annual-v1`
- `input_snapshot.assumptions.assumption_set_id` when an active versioned assumption set is found
- `input_snapshot.assumptions.usage_payload` for wizard usage inputs used by the run
- `input_snapshot.assumptions.climate_zone` for heating, cooling, and solar severity indexes
- `input_snapshot.assumptions.economic_inputs` for discount rate, energy inflation, period, maintenance, subsidies, and energy prices used by the run
- `input_snapshot.assumptions.scoring_rules_json` for scenario comparison score version, weights, thresholds, and BACS class points
- `input_snapshot.selected_solutions[]` for scenario solution assignments and their resolved catalog assumptions when available

The V1 engine is annual and simplified. Results vary by building surface, construction period, compactness, climate indexes, zones, orientation, occupancy, systems, BACS functions, and selected scenario solutions.

### economic result fields
- `total_capex`
- `subsidies`
- `net_capex`
- `baseline_opex_year`
- `scenario_opex_year`
- `energy_cost_savings`
- `maintenance_cost_year`
- `maintenance_savings_year`
- `net_annual_savings`
- `annual_cost_savings`
- `simple_payback_years` (`null` when not calculable)
- `npv`
- `irr` (`null` when not calculable)
- `analysis_period_years`
- `discount_rate`
- `energy_inflation_rate`
- `cash_flows[]`
- `is_roi_calculable`

### scenario comparison scoring fields
- `score`: backward-compatible global score on 0..100
- `scoring_version`: version label from `scoring_rules_json.version`
- `score_breakdown.weights`: normalized weights used for energy, BACS, ROI, and CAPEX
- `score_breakdown.sub_scores`: 0..100 sub-score for each dimension
- `score_breakdown.contributions`: weighted contribution of each dimension to `score`
- `score_breakdown.dominant_contributors`: top dimensions used to explain the recommendation

The comparison endpoint reads scoring rules from each calculation snapshot. If a historical run has no scoring rules, the platform V1 default is applied explicitly by the scoring module.

### solution definition fields
- `id`
- `catalog_id`
- `catalog_name`
- `catalog_version`
- `scope`
- `country_code`
- `organization_id`
- `code`
- `name`
- `description`
- `family`
- `target_scopes`
- `applicable_countries`
- `applicable_building_types`
- `applicable_zone_types`
- `bacs_impact_json`
- `lifetime_years`
- `default_quantity`
- `default_unit`
- `default_unit_cost`
- `default_capex`
- `priority`
- `is_commercial_offer`
- `offer_reference`
- `is_active`

### solution_catalog_scope
- global
- country_specific
- organization_specific

### building_type
- hotel
- aparthotel
- residence
- other_accommodation

### zone_type
- guest_rooms
- circulation
- lobby
- restaurant
- meeting
- technical
- spa
- pool
- other

### orientation
- north
- south
- east
- west
- mixed

### report_type
- executive
- detailed

For the detailed contracts, extend from the earlier specification and implement them in Pydantic schema files.
