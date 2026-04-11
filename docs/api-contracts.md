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
- `/api/v1/admin/branding`
- `/api/v1/admin/branding/{id}`
- `/api/v1/branding`
- `/api/v1/projects`
- `/api/v1/projects/{id}/assumptions`
- `/api/v1/projects/{id}/history`
- `/api/v1/projects/{id}/wizard`
- `/api/v1/projects/{id}/building`
- `/api/v1/projects/{id}/zones`
- `/api/v1/projects/{id}/systems`
- `/api/v1/projects/{id}/bacs`
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
- `/api/v1/reports/{reportId}`
- `/api/v1/reports/{reportId}/download`

Generated report metadata now retains the optional `branding_profile_id` used during rendering.

## Main enums
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
- scenario_created
- scenario_updated
- report_generated

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
