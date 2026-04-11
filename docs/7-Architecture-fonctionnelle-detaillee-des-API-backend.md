
# 7. Architecture fonctionnelle détaillée des API backend

## 7.1 Principes généraux

### Style d’API

* REST JSON
* versionnée par préfixe :

  * `/api/v1/...`

### Format des réponses

Structure recommandée :

```json
{
  "data": {},
  "meta": {},
  "errors": []
}
```

### Dates

* format ISO 8601

### Identifiants

* UUID

### Langue

* portée par :

  * préférence utilisateur,
  * ou header `Accept-Language`,
  * ou champ explicite sur certaines routes de rapport.

### Authentification

* Bearer token
* RBAC côté backend

---

## 7.2 Conventions HTTP

### Méthodes

* `GET` : lecture
* `POST` : création / action métier
* `PATCH` : modification partielle
* `PUT` : remplacement complet si nécessaire
* `DELETE` : suppression logique de préférence

### Codes de retour

* `200` : succès lecture/modification
* `201` : création
* `202` : action acceptée si traitement différé plus tard
* `400` : entrée invalide
* `401` : non authentifié
* `403` : interdit
* `404` : non trouvé
* `409` : conflit métier
* `422` : validation métier
* `500` : erreur interne

---

# 7.3 Domaines d’API

Je recommande les groupes suivants :

1. auth
2. users
3. organizations
4. branding
5. projects
6. templates
7. buildings
8. zones
9. usage profiles
10. systems
11. bacs
12. solution catalogs
13. scenarios
14. calculations
15. results
16. reports
17. admin config
18. audit/history

---

# 7.4 Auth API

## 7.4.1 Login

`POST /api/v1/auth/login`

### Request

```json
{
  "email": "user@example.com",
  "password": "secret"
}
```

### Response

```json
{
  "data": {
    "access_token": "jwt-token",
    "token_type": "bearer",
    "expires_in": 3600,
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "role": "commercial",
      "organization_id": "uuid",
      "preferred_language": "fr"
    }
  }
}
```

---

## 7.4.2 Current user

`GET /api/v1/auth/me`

### Response

```json
{
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "Nicolas",
    "last_name": "X",
    "role": "org_admin",
    "organization_id": "uuid",
    "preferred_language": "fr"
  }
}
```

---

## 7.4.3 Logout

`POST /api/v1/auth/logout`

### Response

```json
{
  "data": {
    "success": true
  }
}
```

---

# 7.5 Users API

## 7.5.1 List users

`GET /api/v1/users`

### Query params

* `role`
* `is_active`
* `page`
* `page_size`

### Response

```json
{
  "data": [
    {
      "id": "uuid",
      "email": "a@company.com",
      "first_name": "Alice",
      "last_name": "Martin",
      "role": "commercial",
      "is_active": true
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 1
  }
}
```

---

## 7.5.2 Create user

`POST /api/v1/users`

```json
{
  "email": "new@company.com",
  "first_name": "Jean",
  "last_name": "Dupont",
  "role": "operator",
  "preferred_language": "fr"
}
```

---

## 7.5.3 Update user

`PATCH /api/v1/users/{user_id}`

```json
{
  "first_name": "Jean-Marc",
  "role": "commercial",
  "is_active": true
}
```

---

# 7.6 Organizations API

## 7.6.1 Get current organization

`GET /api/v1/organizations/current`

## 7.6.2 Update organization

`PATCH /api/v1/organizations/current`

```json
{
  "name": "My Energy Company",
  "default_language": "fr",
  "default_country_code": "FR"
}
```

---

# 7.7 Branding API

## 7.7.1 List branding profiles

`GET /api/v1/branding`

## 7.7.2 Create branding profile

`POST /api/v1/branding`

```json
{
  "name": "Default Brand",
  "primary_color": "#123456",
  "secondary_color": "#eeeeee",
  "accent_color": "#ff9900",
  "report_footer_text": "Confidential document",
  "legal_notice_text": "Internal use only"
}
```

## 7.7.3 Update branding profile

`PATCH /api/v1/branding/{branding_id}`

## 7.7.4 Upload logo

Deux options :

* route dédiée multipart
* ou URL de fichier si stockage séparé

`POST /api/v1/branding/{branding_id}/logo`

---

# 7.8 Projects API

## 7.8.1 List projects

`GET /api/v1/projects`

### Query params

* `status`
* `country_code`
* `building_type`
* `client_name`
* `search`
* `page`
* `page_size`

### Response

```json
{
  "data": [
    {
      "id": "uuid",
      "name": "Hôtel Centre Ville",
      "client_name": "Hotel ABC",
      "status": "in_progress",
      "building_type": "hotel",
      "country_code": "FR",
      "wizard_step": 4,
      "updated_at": "2026-04-05T10:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 1
  }
}
```

---

## 7.8.2 Create project

`POST /api/v1/projects`

```json
{
  "name": "Hôtel Centre Ville",
  "client_name": "Hotel ABC",
  "country_profile_id": "uuid",
  "climate_zone_id": "uuid",
  "building_type": "hotel",
  "project_goal": "energy_savings",
  "language": "fr",
  "branding_profile_id": "uuid",
  "template_id": "uuid"
}
```

### Response

```json
{
  "data": {
    "id": "uuid",
    "status": "draft",
    "wizard_step": 1
  }
}
```

---

## 7.8.3 Get project

`GET /api/v1/projects/{project_id}`

Réponse enrichie avec :

* résumé,
* progression,
* bâtiment,
* stats scénarios.

---

## 7.8.4 Update project

`PATCH /api/v1/projects/{project_id}`

```json
{
  "name": "Hôtel Centre Ville rénové",
  "project_goal": "global_audit",
  "wizard_step": 2
}
```

---

## 7.8.5 Duplicate project

`POST /api/v1/projects/{project_id}/duplicate`

```json
{
  "name": "Copie - Hôtel Centre Ville"
}
```

---

## 7.8.6 Archive project

`POST /api/v1/projects/{project_id}/archive`

---

## 7.8.7 Project overview

`GET /api/v1/projects/{project_id}/overview`

### Response

Retourne :

* infos projet,
* état initial,
* meilleur scénario,
* derniers rapports,
* progression wizard.

---

# 7.9 Project Templates API

## 7.9.1 List templates

`GET /api/v1/project-templates`

## 7.9.2 Create template

`POST /api/v1/project-templates`

```json
{
  "name": "Hôtel urbain standard",
  "description": "Template hôtel avec restaurant",
  "building_type": "hotel",
  "country_profile_id": "uuid",
  "default_payload_json": {}
}
```

## 7.9.3 Create template from project

`POST /api/v1/projects/{project_id}/save-as-template`

---

# 7.10 Building API

## 7.10.1 Get building

`GET /api/v1/projects/{project_id}/building`

## 7.10.2 Create or replace building

`PUT /api/v1/projects/{project_id}/building`

```json
{
  "name": "Bâtiment principal",
  "construction_period": "1975_1990",
  "gross_floor_area_m2": 5000,
  "heated_area_m2": 4200,
  "cooled_area_m2": 3500,
  "number_of_floors": 5,
  "number_of_rooms": 80,
  "main_orientation": "south",
  "compactness_level": "medium",
  "has_restaurant": true,
  "has_meeting_rooms": true,
  "has_spa": false,
  "has_pool": false
}
```

## 7.10.3 Patch building

`PATCH /api/v1/projects/{project_id}/building`

---

# 7.11 Zones API

## 7.11.1 List zones

`GET /api/v1/projects/{project_id}/zones`

## 7.11.2 Auto-generate zones from wizard

`POST /api/v1/projects/{project_id}/zones/generate`

```json
{
  "mode": "express",
  "room_distribution": {
    "north": 20,
    "south": 25,
    "east": 15,
    "west": 20
  },
  "include_common_areas": true,
  "has_restaurant": true,
  "has_meeting_rooms": true
}
```

### Response

Retourne la proposition de zoning.

---

## 7.11.3 Create zone

`POST /api/v1/projects/{project_id}/zones`

```json
{
  "name": "Chambres Sud",
  "zone_type": "guest_rooms",
  "orientation": "south",
  "area_m2": 1200,
  "room_count": 24,
  "window_ratio": 0.35,
  "infiltration_level": "medium",
  "solar_exposure_level": "high",
  "is_conditioned": true
}
```

## 7.11.4 Update zone

`PATCH /api/v1/projects/{project_id}/zones/{zone_id}`

## 7.11.5 Delete zone

`DELETE /api/v1/projects/{project_id}/zones/{zone_id}`

## 7.11.6 Validate zones

`GET /api/v1/projects/{project_id}/zones/validation`

### Response

```json
{
  "data": {
    "is_valid": true,
    "warnings": [
      "La somme des surfaces de zones diffère de 4% de la surface totale."
    ]
  }
}
```

---

# 7.12 Usage Profiles API

## 7.12.1 List default profiles

`GET /api/v1/usage-profiles?country_profile_id=...&building_type=hotel`

## 7.12.2 Get project usage overrides

`GET /api/v1/projects/{project_id}/usage-overrides`

## 7.12.3 Upsert project usage override

`PUT /api/v1/projects/{project_id}/usage-overrides`

```json
{
  "building_zone_id": "uuid",
  "usage_profile_id": "uuid",
  "occupancy_rate_override": 0.72,
  "ecs_intensity_override": "high"
}
```

---

# 7.13 Technical Systems API

## 7.13.1 List systems

`GET /api/v1/projects/{project_id}/systems`

## 7.13.2 Create system

`POST /api/v1/projects/{project_id}/systems`

```json
{
  "system_type": "heating",
  "name": "Chaudière gaz principale",
  "energy_source": "gas",
  "technology_type": "gas_boiler",
  "efficiency_level": "standard",
  "control_level": "basic",
  "is_centralized": true
}
```

## 7.13.3 Update system

`PATCH /api/v1/projects/{project_id}/systems/{system_id}`

## 7.13.4 Delete system

`DELETE /api/v1/projects/{project_id}/systems/{system_id}`

---

# 7.14 BACS API

## 7.14.1 Get current BACS assessment

`GET /api/v1/projects/{project_id}/bacs/current`

## 7.14.2 Initialize current BACS assessment

`POST /api/v1/projects/{project_id}/bacs/current`

```json
{
  "assessment_method": "questionnaire"
}
```

## 7.14.3 Save BACS questionnaire answers

`PUT /api/v1/projects/{project_id}/bacs/current/functions`

```json
{
  "functions": [
    {
      "bacs_function_definition_id": "uuid",
      "status": "present",
      "applies_to_zone_id": "uuid"
    },
    {
      "bacs_function_definition_id": "uuid2",
      "status": "absent"
    }
  ]
}
```

## 7.14.4 Get computed BACS summary

`GET /api/v1/projects/{project_id}/bacs/current/summary`

### Response

```json
{
  "data": {
    "estimated_bacs_class": "C",
    "final_bacs_class": "C",
    "confidence_score": 0.74,
    "score_by_domain": {
      "heating": 45,
      "cooling": 38,
      "ventilation": 52,
      "dhw": 40,
      "lighting": 55,
      "supervision": 30,
      "monitoring": 20,
      "room_automation": 25
    },
    "top_missing_functions": [
      "Mode absence chambres",
      "Fenêtre ouverte",
      "Programmation ventilation"
    ]
  }
}
```

## 7.14.5 Override final class

`PATCH /api/v1/projects/{project_id}/bacs/current`

```json
{
  "manual_override_class": "B",
  "notes": "Override validated by expert"
}
```

---

# 7.15 Solution Catalog API

## 7.15.1 List solution catalogs

`GET /api/v1/solution-catalogs`

## 7.15.2 List solutions

`GET /api/v1/solutions`

### Query params

* `catalog_id`
* `country_code`
* `solution_family`
* `building_type`
* `search`
* `is_commercial_offer`

## 7.15.3 Get solution details

`GET /api/v1/solutions/{solution_id}`

## 7.15.4 Create solution

`POST /api/v1/solutions`

```json
{
  "solution_catalog_id": "uuid",
  "code": "ROOM_AUTOMATION_BASIC",
  "name_fr": "Automatisation chambres - niveau de base",
  "name_en": "Guest room automation - basic",
  "solution_family": "bacs",
  "default_energy_gain_model_json": {
    "type": "percentage",
    "default": {
      "heating": 0.10,
      "cooling": 0.12
    }
  },
  "default_capex_model_json": {
    "type": "per_room",
    "value": 180
  },
  "default_lifetime_years": 12,
  "is_commercial_offer": false
}
```

## 7.15.5 Update solution

`PATCH /api/v1/solutions/{solution_id}`

## 7.15.6 Disable solution

`POST /api/v1/solutions/{solution_id}/disable`

---

# 7.16 Scenarios API

## 7.16.1 List scenarios

`GET /api/v1/projects/{project_id}/scenarios`

## 7.16.2 Create scenario

`POST /api/v1/projects/{project_id}/scenarios`

```json
{
  "name": "Optimisation chambres",
  "description": "Absence + fenêtre ouverte + mode nuit",
  "scenario_type": "custom",
  "derived_from_scenario_id": "uuid"
}
```

## 7.16.3 Update scenario

`PATCH /api/v1/projects/{project_id}/scenarios/{scenario_id}`

## 7.16.4 Duplicate scenario

`POST /api/v1/projects/{project_id}/scenarios/{scenario_id}/duplicate`

## 7.16.5 Delete scenario

`DELETE /api/v1/projects/{project_id}/scenarios/{scenario_id}`

---

## 7.16.6 Add solution to scenario

`POST /api/v1/projects/{project_id}/scenarios/{scenario_id}/solutions`

```json
{
  "solution_definition_id": "uuid",
  "target_scope": "zone",
  "target_zone_id": "uuid",
  "quantity": 24
}
```

## 7.16.7 Update scenario solution

`PATCH /api/v1/projects/{project_id}/scenarios/{scenario_id}/solutions/{scenario_solution_id}`

```json
{
  "capex_override": 5200,
  "gain_override_percent": 0.11,
  "notes": "Offre affinée"
}
```

## 7.16.8 Remove solution from scenario

`DELETE /api/v1/projects/{project_id}/scenarios/{scenario_id}/solutions/{scenario_solution_id}`

---

# 7.17 Calculations API

## 7.17.1 Launch calculation

`POST /api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate`

### Request

```json
{
  "force_recalculation": true
}
```

### Response

```json
{
  "data": {
    "calculation_run_id": "uuid",
    "run_status": "completed"
  }
}
```

Pour la V1, ce calcul peut être synchrone si le moteur reste rapide.

---

## 7.17.2 Get calculation runs

`GET /api/v1/projects/{project_id}/scenarios/{scenario_id}/calculations`

## 7.17.3 Get calculation run details

`GET /api/v1/calculations/{calculation_run_id}`

### Response

Retourne :

* métadonnées,
* version moteur,
* warnings,
* snapshots si autorisé.

---

## 7.17.4 Validate project readiness for calculation

`GET /api/v1/projects/{project_id}/calculation-readiness`

### Response

```json
{
  "data": {
    "is_ready": false,
    "blocking_issues": [
      "Surface chauffée manquante",
      "Aucune zone définie"
    ],
    "warnings": [
      "Le système ECS n'est pas renseigné"
    ],
    "confidence_level": "medium"
  }
}
```

---

# 7.18 Results API

## 7.18.1 Scenario result summary

`GET /api/v1/projects/{project_id}/scenarios/{scenario_id}/results/latest`

### Response

```json
{
  "data": {
    "summary": {
      "baseline_energy_kwh_year": 1200000,
      "scenario_energy_kwh_year": 980000,
      "energy_savings_kwh_year": 220000,
      "energy_savings_percent": 18.3,
      "baseline_co2_kg_year": 145000,
      "scenario_co2_kg_year": 112000,
      "co2_savings_percent": 22.8,
      "baseline_bacs_class": "C",
      "scenario_bacs_class": "B",
      "global_project_score": 74
    },
    "economic": {
      "total_capex": 92000,
      "annual_cost_savings": 28000,
      "simple_payback_years": 3.3,
      "npv": 105000,
      "irr": 0.21
    },
    "messages": [
      "Le chauffage constitue le principal poste de consommation estimé.",
      "Les chambres sud concentrent une part importante du potentiel d'optimisation."
    ]
  }
}
```

---

## 7.18.2 Results by use

`GET /api/v1/calculations/{calculation_run_id}/results/by-use`

## 7.18.3 Results by zone

`GET /api/v1/calculations/{calculation_run_id}/results/by-zone`

## 7.18.4 Economic results

`GET /api/v1/calculations/{calculation_run_id}/results/economic`

## 7.18.5 BACS results

`GET /api/v1/calculations/{calculation_run_id}/results/bacs`

---

## 7.18.6 Compare scenarios

`POST /api/v1/projects/{project_id}/scenarios/compare`

```json
{
  "scenario_ids": [
    "uuid_ref",
    "uuid_a",
    "uuid_b",
    "uuid_c"
  ]
}
```

### Response

Retourne tableau consolidé :

* énergie,
* CO₂,
* BACS,
* CAPEX,
* ROI,
* score global,
* scénario recommandé.

---

# 7.19 Reports API

## 7.19.1 Generate report

`POST /api/v1/projects/{project_id}/reports`

```json
{
  "scenario_id": "uuid",
  "calculation_run_id": "uuid",
  "report_type": "executive",
  "language": "fr",
  "branding_profile_id": "uuid",
  "include_assumptions": true,
  "include_regulatory_section": true,
  "include_annexes": false
}
```

### Response

```json
{
  "data": {
    "report_id": "uuid",
    "generation_status": "generated",
    "download_url": "/api/v1/reports/uuid/download"
  }
}
```

---

## 7.19.2 Generate comparison report

`POST /api/v1/projects/{project_id}/reports/comparison`

```json
{
  "scenario_ids": ["uuid_ref", "uuid_a", "uuid_b"],
  "report_type": "executive",
  "language": "fr"
}
```

---

## 7.19.3 List reports

`GET /api/v1/projects/{project_id}/reports`

## 7.19.4 Get report metadata

`GET /api/v1/reports/{report_id}`

## 7.19.5 Download report

`GET /api/v1/reports/{report_id}/download`

## 7.19.6 Delete report

`DELETE /api/v1/reports/{report_id}`

---

# 7.20 Admin Config API

## 7.20.1 Country profiles

`GET /api/v1/admin/country-profiles`

`PATCH /api/v1/admin/country-profiles/{country_profile_id}`

---

## 7.20.2 Climate zones

`GET /api/v1/admin/climate-zones`

`POST /api/v1/admin/climate-zones`

`PATCH /api/v1/admin/climate-zones/{climate_zone_id}`

---

## 7.20.3 Calculation assumption sets

`GET /api/v1/admin/assumption-sets`

`POST /api/v1/admin/assumption-sets`

`PATCH /api/v1/admin/assumption-sets/{assumption_set_id}`

Exemple :

```json
{
  "name": "Default FR v1",
  "country_profile_id": "uuid",
  "version": "1.0.0",
  "economic_defaults_json": {
    "discount_rate": 0.06,
    "energy_inflation_rate": 0.03,
    "analysis_period_years": 15
  }
}
```

---

## 7.20.4 BACS function definitions

`GET /api/v1/admin/bacs-functions`

`POST /api/v1/admin/bacs-functions`

`PATCH /api/v1/admin/bacs-functions/{function_id}`

---

## 7.20.5 Automatic text rules

`GET /api/v1/admin/text-rules`

`PATCH /api/v1/admin/text-rules/{rule_id}`

Pour les messages automatiques du rapport et des résultats.

---

# 7.21 Audit & History API

## 7.21.1 Project history

`GET /api/v1/projects/{project_id}/history`

## 7.21.2 Scenario history

`GET /api/v1/projects/{project_id}/scenarios/{scenario_id}/history`

## 7.21.3 Audit logs

`GET /api/v1/audit-logs`

Filtres :

* `entity_type`
* `user_id`
* `action`
* `date_from`
* `date_to`

---

# 7.22 Wizard-oriented API design

Pour simplifier le frontend, je recommande aussi des endpoints “orchestrés” par étape.

## 7.22.1 Get wizard state

`GET /api/v1/projects/{project_id}/wizard`

### Response

```json
{
  "data": {
    "current_step": 5,
    "steps": [
      {"step": 1, "name": "project", "status": "completed"},
      {"step": 2, "name": "context", "status": "completed"},
      {"step": 3, "name": "building", "status": "completed"},
      {"step": 4, "name": "zones", "status": "completed"},
      {"step": 5, "name": "usage", "status": "in_progress"},
      {"step": 6, "name": "systems", "status": "not_started"}
    ],
    "readiness": {
      "can_calculate": false,
      "confidence_level": "medium"
    }
  }
}
```

---

## 7.22.2 Save wizard step payload

`PUT /api/v1/projects/{project_id}/wizard/steps/{step_name}`

Exemple pour `building` :

```json
{
  "gross_floor_area_m2": 5000,
  "heated_area_m2": 4200,
  "cooled_area_m2": 3500,
  "number_of_floors": 5,
  "number_of_rooms": 80,
  "construction_period": "1975_1990"
}
```

### Intérêt

Le frontend peut avancer étape par étape sans connaître toute la granularité interne des tables.

---

## 7.22.3 Validate wizard step

`POST /api/v1/projects/{project_id}/wizard/steps/{step_name}/validate`

### Response

```json
{
  "data": {
    "is_valid": true,
    "errors": [],
    "warnings": [
      "Le niveau d'étanchéité n'est pas renseigné : une valeur standard sera utilisée."
    ]
  }
}
```

---

# 7.23 Permissions par domaine

## Super Admin

* tout

## Org Admin

* tout sur son organisation
* branding
* users
* catalogues organisation
* modèles de projets

## Commercial

* CRUD projets
* scénarios
* calculs
* rapports
* lecture catalogue
* pas de modif admin profonde

## Operator

* CRUD projets
* scénarios
* calculs
* rapports
* moins orienté branding

## Viewer

* lecture seule
* téléchargement rapports

---

# 7.24 Endpoints prioritaires MVP

Si on veut un MVP efficace, je prioriserais :

### Auth

* login
* me

### Projects

* create/list/get/update
* duplicate
* overview

### Wizard

* get wizard
* save step
* validate step

### Building / zones / systems

* CRUD minimal

### BACS

* get/save questionnaire
* get summary

### Scenarios

* create/update/list
* add/remove solution

### Calcul

* readiness
* calculate
* latest results
* compare scenarios

### Reports

* generate
* list
* download

---

# 7.25 Recommandations de structure FastAPI

Je recommande une structure de routes du type :

```text
app/api/v1/
  auth.py
  users.py
  organizations.py
  branding.py
  projects.py
  wizard.py
  buildings.py
  zones.py
  usage_profiles.py
  systems.py
  bacs.py
  solutions.py
  scenarios.py
  calculations.py
  results.py
  reports.py
  admin_config.py
  audit_logs.py
```

Avec séparation :

* `schemas/` pour Pydantic
* `services/` pour logique métier
* `repositories/` pour accès DB
* `domain/` ou `calculation/` pour moteur de calcul

---

# 7.26 Exemples de schémas Pydantic

## ProjectCreate

```python
class ProjectCreate(BaseModel):
    name: str
    client_name: str | None = None
    country_profile_id: UUID
    climate_zone_id: UUID
    building_type: Literal["hotel", "aparthotel", "residence", "other_accommodation"]
    project_goal: str | None = None
    branding_profile_id: UUID | None = None
    template_id: UUID | None = None
```

## ScenarioCalculateRequest

```python
class ScenarioCalculateRequest(BaseModel):
    force_recalculation: bool = False
```

## ReportGenerateRequest

```python
class ReportGenerateRequest(BaseModel):
    scenario_id: UUID
    calculation_run_id: UUID
    report_type: Literal["executive", "detailed"]
    language: Literal["fr", "en"] = "fr"
    branding_profile_id: UUID | None = None
    include_assumptions: bool = True
    include_regulatory_section: bool = True
    include_annexes: bool = False
```

---

# 7.27 Décisions d’API que je recommande de figer

Je recommande de figer :

* préfixe `/api/v1`
* REST JSON
* UUID partout
* endpoints CRUD + endpoints métier
* endpoints wizard dédiés
* calcul lancé explicitement
* rapports rattachés à un `calculation_run`
* comparaison scénarios par endpoint dédié
* configuration admin séparée des APIs projet
* RBAC clair dès la V1

---
