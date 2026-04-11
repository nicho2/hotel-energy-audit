# Backend Reporting

The reporting module follows the MVP pipeline:

1. load project, scenario, calculation results, building data, zones and branding;
2. build a serializable report context;
3. render an HTML/Jinja template;
4. generate and store a PDF artifact;
5. persist `GeneratedReport` metadata.

## Report Types

Supported report types:

- `executive`: concise decision-support report, using `executive/report.html`.
- `detailed`: extended technical report, using `detailed/report.html`.

The detailed report reuses the executive cover and summary sections, then adds:

- building description;
- zone detail;
- system detail;
- BACS analysis by domain;
- scenario comparison;
- economic analysis;
- assumptions and limits;
- optional regulatory context;
- optional technical annexes.

## Detailed Flags

Detailed rendering is controlled by:

- `include_assumptions`: includes the assumptions and limits section.
- `include_regulatory_section`: includes the regulatory context note.
- `include_annexes`: includes technical annexes with messages, warnings and by-use/by-zone results.

These flags are passed through both HTML rendering and PDF generation paths.

## API

The generic generation endpoint is:

`POST /api/v1/projects/{project_id}/reports`

Request fields:

- `scenario_id`
- `calculation_run_id`
- `report_type`: `executive` or `detailed`
- `language`: `fr` or `en`
- `branding_profile_id`: accepted for contract compatibility; current rendering resolves branding from the project/default organization profile.
- `include_assumptions`
- `include_regulatory_section`
- `include_annexes`

Existing executive endpoints remain supported:

- `GET /api/v1/reports/executive/{calculation_run_id}/html`
- `POST /api/v1/reports/executive/{calculation_run_id}/generate`

Detailed convenience endpoints are also available:

- `GET /api/v1/reports/detailed/{calculation_run_id}/html`
- `POST /api/v1/reports/detailed/{calculation_run_id}/generate`

## Guardrails

The detailed report stays within the simplified annual estimation scope. It exposes snapshots and limits for traceability, but it must not be presented as a dynamic simulation or a regulatory compliance report.
