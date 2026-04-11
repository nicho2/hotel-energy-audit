# Audit Logging

The backend keeps a persistent audit trail for the main business actions. The goal is traceability for operators and technical management, not a full observability or SIEM system.

## Stored Fields

Each audit log stores:

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

`project_id` and `scenario_id` are optional context fields used to make project and scenario history queries stable without parsing JSON payloads.

## Logged Actions

The current implementation logs:

- `project_created`
- `project_updated`
- `project_archived`
- `scenario_created`
- `scenario_updated`
- `scenario_deleted`
- `scenario_calculated`
- `report_generated`
- `assumption_set_updated`
- `solution_created`
- `solution_updated`
- `solution_deactivated`

The payloads are intentionally compact. They include identifiers, names, status, version/scope metadata and changed fields. They do not store passwords, tokens, password hashes, or raw calculation snapshots.

## History Endpoints

Project history:

`GET /api/v1/projects/{project_id}/history`

Scenario history:

`GET /api/v1/projects/{project_id}/scenarios/{scenario_id}/history`

For objects created before audit logging existed, project and scenario history keep a legacy fallback based on timestamps from projects, scenarios and generated reports.

## Admin Audit Query

Admin users can query organization-scoped audit logs:

`GET /api/v1/admin/audit-logs`

Supported filters:

- `entity_type`
- `entity_id`
- `action`
- `project_id`
- `scenario_id`
- `user_id`
- `date_from`
- `date_to`
- `limit`

All queries are scoped to the current user's organization. Logs from another organization are not returned even when the entity identifier is known.

## Noise Control

The audit trail focuses on meaningful business transitions:

- object creation and configuration changes;
- scenario lifecycle operations;
- calculation and report generation;
- sensitive admin configuration updates.

Read-only operations, list views and HTML report previews are not audited.
