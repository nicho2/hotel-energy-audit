# Backend Security Baseline

This MVP uses a simple security model focused on effective tenant isolation and safe access to generated artifacts.

## Authentication

Authentication uses bearer JWT access tokens issued by:

`POST /api/v1/auth/login`

Passwords are stored with PBKDF2-SHA256 and per-password salts. JWTs include:

- `sub`: user id
- `organization_id`
- `email`
- `role`
- `type=access`
- `iat`
- `exp`

On every authenticated request the backend reloads the user from the database and verifies that:

- the user exists;
- the user is active;
- the token is an access token;
- the token organization claim matches the current user organization;
- the token role claim still matches the current user role.

This means a role or organization change invalidates older tokens from an authorization point of view.

## Authorization Guards

Reusable dependencies are available in `app.api.deps.auth`:

- `get_current_user`
- `require_role(...)`
- `require_org_admin`
- `require_project_access`

Admin endpoints use the org-admin guard. Project access checks resolve projects through the current user's organization.

## Organization Isolation

The backend treats missing access and missing resources the same way for tenant-owned objects. Cross-organization project and report access returns `404`, avoiding resource enumeration.

Critical repositories and services scope by `organization_id` for:

- projects;
- branding profiles;
- reports;
- admin users;
- audit logs;
- organization-specific solution catalogs;
- assumption-set overrides.

## Report Downloads

Report metadata is first loaded with the current user's organization id. The file path is then resolved below the configured report storage root.

Download is rejected when:

- the report id does not belong to the current organization;
- the stored path is absolute;
- the stored path contains `..`;
- the resolved file path escapes the report storage directory;
- the file is missing.

## Branding Assets

The current MVP stores branding text and colors, not uploaded binary logo files. Branding profile access is organization-scoped. If binary branding assets are added later, they should follow the same ownership and path-resolution rules as report artifacts.

## Validation

Payload validation combines Pydantic constraints and service-level business checks. Security-relevant validation includes:

- bounded password length on login;
- admin user role constraints;
- project ownership checks before object access;
- active-user checks on every authenticated request;
- report storage path traversal protection.

## Out of Scope

The MVP does not include SSO, enterprise OAuth, WAF integration, advanced rate limiting, or SIEM export.
