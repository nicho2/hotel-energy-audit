
---

# 8. Contrats JSON détaillés

## 8.1 Principes généraux

### Format de réponse standard

Je recommande de figer ce format pour **toutes** les réponses API :

```json
{
  "data": {},
  "meta": {},
  "errors": []
}
```

### Cas d’usage

* `data` : contenu métier principal
* `meta` : pagination, version, warnings, infos annexes
* `errors` : erreurs métier ou validation

### En cas d’erreur bloquante

Le backend peut renvoyer :

```json
{
  "data": null,
  "meta": {},
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "The request payload is invalid.",
      "field": "gross_floor_area_m2",
      "details": {
        "expected": "positive number"
      }
    }
  ]
}
```

---

## 8.2 Convention d’erreurs

## Structure d’une erreur

```json
{
  "code": "VALIDATION_ERROR",
  "message": "The request payload is invalid.",
  "field": "gross_floor_area_m2",
  "details": {
    "reason": "must be greater than zero"
  }
}
```

## Champs

* `code` : code stable lisible par le frontend
* `message` : message lisible
* `field` : champ concerné si applicable
* `details` : objet libre

## Codes recommandés

* `VALIDATION_ERROR`
* `NOT_FOUND`
* `FORBIDDEN`
* `UNAUTHORIZED`
* `CONFLICT`
* `BUSINESS_RULE_ERROR`
* `CALCULATION_NOT_READY`
* `REPORT_GENERATION_FAILED`
* `INTERNAL_ERROR`

---

## 8.3 Convention meta

### Exemple standard

```json
{
  "meta": {
    "request_id": "uuid",
    "timestamp": "2026-04-05T10:15:00Z",
    "version": "v1"
  }
}
```

### Pagination

```json
{
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 135,
    "total_pages": 7
  }
}
```

### Warnings

```json
{
  "meta": {
    "warnings": [
      "Some values were defaulted because no advanced data was provided."
    ]
  }
}
```

---

# 8.4 Contrats Auth

## 8.4.1 `POST /api/v1/auth/login`

### Request

```json
{
  "email": "user@example.com",
  "password": "secret-password"
}
```

### Response 200

```json
{
  "data": {
    "access_token": "jwt-token",
    "token_type": "bearer",
    "expires_in": 3600,
    "user": {
      "id": "9e9fd8cf-8d7f-4c1f-b5d2-83c3cf6e0b8c",
      "organization_id": "289eb76c-f3cf-4737-80fe-d2d33d0632a0",
      "email": "user@example.com",
      "first_name": "Jean",
      "last_name": "Martin",
      "role": "commercial",
      "preferred_language": "fr",
      "is_active": true
    }
  },
  "meta": {
    "version": "v1"
  },
  "errors": []
}
```

### Validation

* `email` obligatoire, format email
* `password` obligatoire, min length configurable

---

## 8.4.2 `GET /api/v1/auth/me`

### Response 200

```json
{
  "data": {
    "id": "9e9fd8cf-8d7f-4c1f-b5d2-83c3cf6e0b8c",
    "organization_id": "289eb76c-f3cf-4737-80fe-d2d33d0632a0",
    "email": "user@example.com",
    "first_name": "Jean",
    "last_name": "Martin",
    "role": "commercial",
    "preferred_language": "fr",
    "is_active": true
  },
  "meta": {},
  "errors": []
}
```

---

# 8.5 Contrats Project

## 8.5.1 `POST /api/v1/projects`

### Request

```json
{
  "name": "Hôtel Centre Ville",
  "client_name": "Hotel ABC",
  "country_profile_id": "8cbbe88b-96ce-4fb7-bae0-e69ab5f95bb9",
  "climate_zone_id": "9b9ef70d-e2c3-4774-b8f4-b795a2b0a44f",
  "building_type": "hotel",
  "project_goal": "energy_savings",
  "branding_profile_id": "d9e7efda-e7f0-4302-bc46-83599a4d6c63",
  "template_id": null
}
```

### Validation

* `name` obligatoire, 3–255 caractères
* `country_profile_id` obligatoire
* `climate_zone_id` obligatoire
* `building_type` dans :

  * `hotel`
  * `aparthotel`
  * `residence`
  * `other_accommodation`

### Response 201

```json
{
  "data": {
    "id": "1b1f44b2-dc2d-45bc-a0b4-52ea68eb5fd7",
    "organization_id": "289eb76c-f3cf-4737-80fe-d2d33d0632a0",
    "name": "Hôtel Centre Ville",
    "client_name": "Hotel ABC",
    "status": "draft",
    "wizard_step": 1,
    "building_type": "hotel",
    "project_goal": "energy_savings",
    "country_profile_id": "8cbbe88b-96ce-4fb7-bae0-e69ab5f95bb9",
    "climate_zone_id": "9b9ef70d-e2c3-4774-b8f4-b795a2b0a44f",
    "branding_profile_id": "d9e7efda-e7f0-4302-bc46-83599a4d6c63",
    "created_at": "2026-04-05T10:20:00Z",
    "updated_at": "2026-04-05T10:20:00Z"
  },
  "meta": {},
  "errors": []
}
```

---

## 8.5.2 `GET /api/v1/projects/{project_id}`

### Response 200

```json
{
  "data": {
    "id": "1b1f44b2-dc2d-45bc-a0b4-52ea68eb5fd7",
    "name": "Hôtel Centre Ville",
    "client_name": "Hotel ABC",
    "reference_code": "HTL-2026-001",
    "description": null,
    "status": "in_progress",
    "wizard_step": 4,
    "building_type": "hotel",
    "project_goal": "energy_savings",
    "country_profile": {
      "id": "8cbbe88b-96ce-4fb7-bae0-e69ab5f95bb9",
      "country_code": "FR",
      "name": "France"
    },
    "climate_zone": {
      "id": "9b9ef70d-e2c3-4774-b8f4-b795a2b0a44f",
      "code": "H3C3",
      "name": "France tempérée"
    },
    "branding_profile_id": "d9e7efda-e7f0-4302-bc46-83599a4d6c63",
    "created_at": "2026-04-05T10:20:00Z",
    "updated_at": "2026-04-05T10:35:00Z"
  },
  "meta": {
    "completeness": {
      "project": "completed",
      "building": "completed",
      "zones": "in_progress",
      "usage": "not_started",
      "systems": "not_started",
      "bacs": "not_started",
      "scenarios": "not_started"
    }
  },
  "errors": []
}
```

---

## 8.5.3 `PATCH /api/v1/projects/{project_id}`

### Request

```json
{
  "name": "Hôtel Centre Ville - Audit énergétique",
  "project_goal": "global_audit",
  "wizard_step": 5
}
```

### Response 200

```json
{
  "data": {
    "id": "1b1f44b2-dc2d-45bc-a0b4-52ea68eb5fd7",
    "name": "Hôtel Centre Ville - Audit énergétique",
    "project_goal": "global_audit",
    "wizard_step": 5,
    "updated_at": "2026-04-05T10:40:00Z"
  },
  "meta": {},
  "errors": []
}
```

---

# 8.6 Contrats Wizard

## 8.6.1 `GET /api/v1/projects/{project_id}/wizard`

### Response 200

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
      {"step": 6, "name": "systems", "status": "not_started"},
      {"step": 7, "name": "bacs", "status": "not_started"},
      {"step": 8, "name": "scenarios", "status": "not_started"},
      {"step": 9, "name": "results", "status": "locked"},
      {"step": 10, "name": "report", "status": "locked"}
    ],
    "readiness": {
      "can_calculate": false,
      "confidence_level": "medium"
    }
  },
  "meta": {},
  "errors": []
}
```

---

## 8.6.2 `PUT /api/v1/projects/{project_id}/wizard/steps/building`

### Request

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

### Validation

* `gross_floor_area_m2 > 0`
* `heated_area_m2 <= gross_floor_area_m2`
* `cooled_area_m2 <= gross_floor_area_m2`
* `number_of_floors >= 1`
* `number_of_rooms >= 0`

### Response 200

```json
{
  "data": {
    "step": "building",
    "status": "saved",
    "building_id": "4a2f6e0f-1d6a-49ef-8146-9ec9bf6cb50c"
  },
  "meta": {
    "warnings": []
  },
  "errors": []
}
```

---

## 8.6.3 `POST /api/v1/projects/{project_id}/wizard/steps/building/validate`

### Response 200

```json
{
  "data": {
    "is_valid": true,
    "errors": [],
    "warnings": [
      "No infiltration level was provided. A default value will be used."
    ]
  },
  "meta": {},
  "errors": []
}
```

---

# 8.7 Contrats Building

## 8.7.1 `GET /api/v1/projects/{project_id}/building`

### Response 200

```json
{
  "data": {
    "id": "4a2f6e0f-1d6a-49ef-8146-9ec9bf6cb50c",
    "project_id": "1b1f44b2-dc2d-45bc-a0b4-52ea68eb5fd7",
    "name": "Bâtiment principal",
    "construction_period": "1975_1990",
    "year_of_construction": null,
    "gross_floor_area_m2": 5000,
    "heated_area_m2": 4200,
    "cooled_area_m2": 3500,
    "number_of_floors": 5,
    "number_of_rooms": 80,
    "average_floor_height_m": null,
    "main_orientation": "south",
    "compactness_level": "medium",
    "has_restaurant": true,
    "has_meeting_rooms": true,
    "has_spa": false,
    "has_pool": false,
    "notes": null
  },
  "meta": {},
  "errors": []
}
```

---

# 8.8 Contrats Zones

## 8.8.1 `POST /api/v1/projects/{project_id}/zones/generate`

### Request

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

### Response 200

```json
{
  "data": {
    "proposed_zones": [
      {
        "name": "Chambres Nord",
        "zone_type": "guest_rooms",
        "orientation": "north",
        "area_m2": 900,
        "room_count": 20,
        "window_ratio": 0.25,
        "infiltration_level": "medium",
        "solar_exposure_level": "low",
        "is_conditioned": true
      },
      {
        "name": "Chambres Sud",
        "zone_type": "guest_rooms",
        "orientation": "south",
        "area_m2": 1125,
        "room_count": 25,
        "window_ratio": 0.35,
        "infiltration_level": "medium",
        "solar_exposure_level": "high",
        "is_conditioned": true
      }
    ]
  },
  "meta": {
    "warnings": [
      "Areas were estimated from the number of rooms using default ratios."
    ]
  },
  "errors": []
}
```

---

## 8.8.2 `POST /api/v1/projects/{project_id}/zones`

### Request

```json
{
  "name": "Chambres Sud",
  "zone_type": "guest_rooms",
  "orientation": "south",
  "floor_index": null,
  "area_m2": 1125,
  "volume_m3": null,
  "room_count": 25,
  "window_ratio": 0.35,
  "occupancy_profile_id": null,
  "heating_setpoint_c": 21,
  "cooling_setpoint_c": 24,
  "night_setback_enabled": true,
  "infiltration_level": "medium",
  "solar_exposure_level": "high",
  "is_conditioned": true,
  "notes": null
}
```

### Validation

* `zone_type` dans la liste autorisée
* `orientation` dans `north|south|east|west|mixed`
* `area_m2 > 0`
* `window_ratio` entre `0` et `1`

### Response 201

```json
{
  "data": {
    "id": "0fa41d8e-146a-4ce7-a44b-7fd1b64f3645",
    "name": "Chambres Sud",
    "zone_type": "guest_rooms",
    "orientation": "south",
    "area_m2": 1125,
    "room_count": 25
  },
  "meta": {},
  "errors": []
}
```

---

## 8.8.3 `GET /api/v1/projects/{project_id}/zones/validation`

### Response 200

```json
{
  "data": {
    "is_valid": true,
    "checks": [
      {
        "code": "TOTAL_AREA_MATCH",
        "status": "warning",
        "message": "The sum of zone areas differs from gross floor area by 3.8%."
      },
      {
        "code": "ROOM_COUNT_MATCH",
        "status": "ok",
        "message": "The total room count matches the building room count."
      }
    ]
  },
  "meta": {},
  "errors": []
}
```

---

# 8.9 Contrats Usage Overrides

## 8.9.1 `PUT /api/v1/projects/{project_id}/usage-overrides`

### Request

```json
{
  "building_zone_id": "0fa41d8e-146a-4ce7-a44b-7fd1b64f3645",
  "usage_profile_id": "6bf7cd32-f4ea-4d4f-8e65-548ef2145c2c",
  "occupancy_rate_override": 0.72,
  "seasonality_profile_override_json": {
    "jan": 0.55,
    "feb": 0.60,
    "mar": 0.68,
    "apr": 0.72,
    "may": 0.75,
    "jun": 0.78,
    "jul": 0.90,
    "aug": 0.92,
    "sep": 0.76,
    "oct": 0.70,
    "nov": 0.62,
    "dec": 0.58
  },
  "ecs_intensity_override": "high",
  "lighting_intensity_override": "standard",
  "notes": null
}
```

### Validation

* `occupancy_rate_override` entre `0` et `1`
* mois obligatoires si profil mensuel fourni

### Response 200

```json
{
  "data": {
    "id": "4f5a183b-0bcf-4320-ab2e-6806efecb728",
    "project_id": "1b1f44b2-dc2d-45bc-a0b4-52ea68eb5fd7",
    "building_zone_id": "0fa41d8e-146a-4ce7-a44b-7fd1b64f3645",
    "usage_profile_id": "6bf7cd32-f4ea-4d4f-8e65-548ef2145c2c",
    "occupancy_rate_override": 0.72
  },
  "meta": {},
  "errors": []
}
```

---

# 8.10 Contrats Systems

## 8.10.1 `POST /api/v1/projects/{project_id}/systems`

### Request

```json
{
  "system_type": "heating",
  "name": "Chaudière gaz principale",
  "serves_zone_id": null,
  "energy_source": "gas",
  "technology_type": "gas_boiler",
  "efficiency_level": "standard",
  "distribution_type": "water_loop",
  "terminal_type": "radiators",
  "control_level": "basic",
  "nominal_power_kw": 350,
  "operation_schedule_type": "day_extended",
  "age_band": "10_15_years",
  "is_centralized": true,
  "notes": null
}
```

### Validation

* `system_type` obligatoire
* `energy_source` obligatoire selon `system_type`
* `nominal_power_kw > 0` si fourni

### Response 201

```json
{
  "data": {
    "id": "4d3e7914-2160-427a-8268-19e31756f68b",
    "system_type": "heating",
    "name": "Chaudière gaz principale",
    "energy_source": "gas",
    "efficiency_level": "standard",
    "control_level": "basic"
  },
  "meta": {},
  "errors": []
}
```

---

# 8.11 Contrats BACS

## 8.11.1 `PUT /api/v1/projects/{project_id}/bacs/current/functions`

### Request

```json
{
  "functions": [
    {
      "bacs_function_definition_id": "0c0fd7d3-a34a-4130-9dd2-2fc9314e60f2",
      "status": "present",
      "applies_to_zone_id": "0fa41d8e-146a-4ce7-a44b-7fd1b64f3645",
      "manual_gain_adjustment_percent": null,
      "notes": null
    },
    {
      "bacs_function_definition_id": "1d6fdfbc-e6c0-4509-9b3b-bdf5f7459ca5",
      "status": "absent",
      "applies_to_zone_id": null,
      "manual_gain_adjustment_percent": null,
      "notes": null
    }
  ]
}
```

### Validation

* `status` dans :

  * `present`
  * `absent`
  * `planned`

### Response 200

```json
{
  "data": {
    "assessment_id": "d8b9dbbf-f1f7-4b8b-b2c7-fbd236d3a5c3",
    "saved_count": 2
  },
  "meta": {},
  "errors": []
}
```

---

## 8.11.2 `GET /api/v1/projects/{project_id}/bacs/current/summary`

### Response 200

```json
{
  "data": {
    "assessment_id": "d8b9dbbf-f1f7-4b8b-b2c7-fbd236d3a5c3",
    "assessment_method": "questionnaire",
    "estimated_bacs_class": "C",
    "manual_override_class": null,
    "final_bacs_class": "C",
    "confidence_score": 0.74,
    "score_global": 52,
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
      {
        "code": "ROOM_ABSENCE_MODE",
        "label": "Mode absence chambres",
        "impact_level": "high"
      },
      {
        "code": "WINDOW_OPEN_DETECTION",
        "label": "Détection fenêtre ouverte",
        "impact_level": "high"
      }
    ]
  },
  "meta": {},
  "errors": []
}
```

---

# 8.12 Contrats Solutions

## 8.12.1 `GET /api/v1/solutions/{solution_id}`

### Response 200

```json
{
  "data": {
    "id": "884183c0-0a0f-45bd-8436-b818438ae534",
    "solution_catalog_id": "94fb8fb7-a1ea-443d-a65f-f1a02661fdbe",
    "code": "ROOM_AUTOMATION_BASIC",
    "name_fr": "Automatisation chambres - niveau de base",
    "name_en": "Guest room automation - basic",
    "description_fr": "Automatisation de fonctions de confort et d'économie dans les chambres.",
    "description_en": "Automation of comfort and energy-saving functions in guest rooms.",
    "solution_family": "bacs",
    "applicable_building_types_json": ["hotel", "aparthotel"],
    "applicable_zone_types_json": ["guest_rooms"],
    "applicable_country_codes_json": ["FR", "DE", "ES"],
    "default_energy_gain_model_json": {
      "type": "percentage",
      "default": {
        "heating": 0.10,
        "cooling": 0.12,
        "lighting": 0.15
      },
      "orientation_bonus": {
        "south": {
          "cooling": 0.03
        }
      }
    },
    "default_capex_model_json": {
      "type": "per_room",
      "value": 180
    },
    "default_maintenance_model_json": {
      "type": "percent_of_capex",
      "value": 0.02
    },
    "default_lifetime_years": 12,
    "default_bacs_class_impact_json": {
      "room_automation": 18
    },
    "priority_order": 10,
    "is_commercial_offer": false,
    "offer_reference": null,
    "is_active": true,
    "version": "1.0.0"
  },
  "meta": {},
  "errors": []
}
```

---

# 8.13 Contrats Scenarios

## 8.13.1 `POST /api/v1/projects/{project_id}/scenarios`

### Request

```json
{
  "name": "Optimisation chambres",
  "description": "Absence + fenêtre ouverte + mode nuit",
  "scenario_type": "custom",
  "derived_from_scenario_id": null
}
```

### Response 201

```json
{
  "data": {
    "id": "1bcd6075-c946-4a77-a43b-5e0dd2dfedab",
    "project_id": "1b1f44b2-dc2d-45bc-a0b4-52ea68eb5fd7",
    "name": "Optimisation chambres",
    "description": "Absence + fenêtre ouverte + mode nuit",
    "scenario_type": "custom",
    "is_reference": false,
    "status": "draft",
    "created_at": "2026-04-05T10:55:00Z"
  },
  "meta": {},
  "errors": []
}
```

---

## 8.13.2 `POST /api/v1/projects/{project_id}/scenarios/{scenario_id}/solutions`

### Request

```json
{
  "solution_definition_id": "884183c0-0a0f-45bd-8436-b818438ae534",
  "target_scope": "zone",
  "target_zone_id": "0fa41d8e-146a-4ce7-a44b-7fd1b64f3645",
  "target_system_id": null,
  "quantity": 25,
  "unit_cost_override": null,
  "capex_override": null,
  "maintenance_override": null,
  "gain_override_percent": null,
  "notes": null
}
```

### Response 201

```json
{
  "data": {
    "id": "4868a921-ffcb-4e18-bad6-b0332b50d9b5",
    "scenario_id": "1bcd6075-c946-4a77-a43b-5e0dd2dfedab",
    "solution_definition_id": "884183c0-0a0f-45bd-8436-b818438ae534",
    "target_scope": "zone",
    "target_zone_id": "0fa41d8e-146a-4ce7-a44b-7fd1b64f3645",
    "quantity": 25,
    "is_selected": true
  },
  "meta": {},
  "errors": []
}
```

---

# 8.14 Contrats Calculation Readiness

## 8.14.1 `GET /api/v1/projects/{project_id}/calculation-readiness`

### Response 200

```json
{
  "data": {
    "is_ready": false,
    "blocking_issues": [
      {
        "code": "MISSING_BUILDING",
        "message": "Building data is missing."
      },
      {
        "code": "NO_ZONES_DEFINED",
        "message": "At least one zone must be defined."
      }
    ],
    "warnings": [
      {
        "code": "MISSING_DHW_SYSTEM",
        "message": "No DHW system was provided. A standard assumption will be used."
      }
    ],
    "confidence_level": "medium"
  },
  "meta": {},
  "errors": []
}
```

---

# 8.15 Contrats Calculations

## 8.15.1 `POST /api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate`

### Request

```json
{
  "force_recalculation": true
}
```

### Response 200

```json
{
  "data": {
    "calculation_run_id": "46604888-f6f2-47a1-90ff-100ea4cbcf3f",
    "scenario_id": "1bcd6075-c946-4a77-a43b-5e0dd2dfedab",
    "run_status": "completed",
    "engine_version": "1.0.0",
    "assumption_set_version": "FR-default-1.0.0",
    "started_at": "2026-04-05T11:00:00Z",
    "finished_at": "2026-04-05T11:00:01Z"
  },
  "meta": {
    "warnings": [
      "The infiltration level was defaulted to 'medium' for 2 zones."
    ]
  },
  "errors": []
}
```

### Réponse alternative si non prêt

HTTP `422`

```json
{
  "data": null,
  "meta": {},
  "errors": [
    {
      "code": "CALCULATION_NOT_READY",
      "message": "Scenario cannot be calculated yet.",
      "details": {
        "blocking_issues": [
          "No zones defined"
        ]
      }
    }
  ]
}
```

---

## 8.15.2 `GET /api/v1/calculations/{calculation_run_id}`

### Response 200

```json
{
  "data": {
    "id": "46604888-f6f2-47a1-90ff-100ea4cbcf3f",
    "scenario_id": "1bcd6075-c946-4a77-a43b-5e0dd2dfedab",
    "run_status": "completed",
    "engine_version": "1.0.0",
    "assumption_set_version": "FR-default-1.0.0",
    "solution_catalog_version_snapshot": "catalog-fr-1.0.0",
    "started_at": "2026-04-05T11:00:00Z",
    "finished_at": "2026-04-05T11:00:01Z",
    "warnings_json": [
      "The infiltration level was defaulted to 'medium' for 2 zones."
    ],
    "errors_json": []
  },
  "meta": {},
  "errors": []
}
```

---

# 8.16 Contrats Results

## 8.16.1 `GET /api/v1/projects/{project_id}/scenarios/{scenario_id}/results/latest`

### Response 200

```json
{
  "data": {
    "summary": {
      "calculation_run_id": "46604888-f6f2-47a1-90ff-100ea4cbcf3f",
      "baseline_energy_kwh_year": 1200000,
      "scenario_energy_kwh_year": 980000,
      "energy_savings_kwh_year": 220000,
      "energy_savings_percent": 18.3,
      "baseline_energy_intensity_kwh_m2": 240,
      "scenario_energy_intensity_kwh_m2": 196,
      "baseline_co2_kg_year": 145000,
      "scenario_co2_kg_year": 112000,
      "co2_savings_kg_year": 33000,
      "co2_savings_percent": 22.8,
      "baseline_bacs_class": "C",
      "scenario_bacs_class": "B",
      "comfort_score_delta": 8,
      "global_project_score": 74
    },
    "economic": {
      "total_capex": 92000,
      "annual_energy_cost_before": 168000,
      "annual_energy_cost_after": 140000,
      "annual_cost_savings": 28000,
      "annual_maintenance_before": 12000,
      "annual_maintenance_after": 10000,
      "annual_maintenance_savings": 2000,
      "simple_payback_years": 3.1,
      "npv": 105000,
      "irr": 0.21,
      "discount_rate": 0.06,
      "energy_inflation_rate": 0.03,
      "analysis_period_years": 15,
      "subsidies_amount": 5000
    },
    "messages": [
      "Le chauffage constitue le principal poste de consommation estimé.",
      "Les chambres sud concentrent une part importante du potentiel d'optimisation.",
      "Le scénario améliore la classe BACS estimée de C vers B."
    ]
  },
  "meta": {},
  "errors": []
}
```

---

## 8.16.2 `GET /api/v1/calculations/{calculation_run_id}/results/by-use`

### Response 200

```json
{
  "data": [
    {
      "use_type": "heating",
      "baseline_kwh_year": 480000,
      "scenario_kwh_year": 390000,
      "savings_kwh_year": 90000,
      "savings_percent": 18.75,
      "co2_baseline_kg_year": 52000,
      "co2_scenario_kg_year": 43000
    },
    {
      "use_type": "cooling",
      "baseline_kwh_year": 180000,
      "scenario_kwh_year": 130000,
      "savings_kwh_year": 50000,
      "savings_percent": 27.8,
      "co2_baseline_kg_year": 9900,
      "co2_scenario_kg_year": 7150
    }
  ],
  "meta": {},
  "errors": []
}
```

---

## 8.16.3 `GET /api/v1/calculations/{calculation_run_id}/results/by-zone`

### Response 200

```json
{
  "data": [
    {
      "building_zone_id": "0fa41d8e-146a-4ce7-a44b-7fd1b64f3645",
      "zone_name": "Chambres Sud",
      "baseline_kwh_year": 260000,
      "scenario_kwh_year": 195000,
      "savings_kwh_year": 65000,
      "savings_percent": 25.0,
      "main_gain_driver": "Room automation"
    },
    {
      "building_zone_id": "31d6e4cc-6f84-4b40-a7d4-e91eea0f812c",
      "zone_name": "Circulations",
      "baseline_kwh_year": 60000,
      "scenario_kwh_year": 50000,
      "savings_kwh_year": 10000,
      "savings_percent": 16.7,
      "main_gain_driver": "Lighting presence detection"
    }
  ],
  "meta": {},
  "errors": []
}
```

---

## 8.16.4 `POST /api/v1/projects/{project_id}/scenarios/compare`

### Request

```json
{
  "scenario_ids": [
    "scenario-ref-uuid",
    "scenario-a-uuid",
    "scenario-b-uuid",
    "scenario-c-uuid"
  ]
}
```

### Response 200

```json
{
  "data": {
    "reference_scenario_id": "scenario-ref-uuid",
    "recommended_scenario_id": "scenario-b-uuid",
    "comparison": [
      {
        "scenario_id": "scenario-ref-uuid",
        "name": "Référence",
        "energy_kwh_year": 1200000,
        "energy_savings_percent": 0,
        "co2_kg_year": 145000,
        "co2_savings_percent": 0,
        "bacs_class": "C",
        "total_capex": 0,
        "annual_cost_savings": 0,
        "simple_payback_years": null,
        "npv": null,
        "irr": null,
        "global_project_score": 48
      },
      {
        "scenario_id": "scenario-b-uuid",
        "name": "Bouquet recommandé",
        "energy_kwh_year": 930000,
        "energy_savings_percent": 22.5,
        "co2_kg_year": 108000,
        "co2_savings_percent": 25.5,
        "bacs_class": "B",
        "total_capex": 98000,
        "annual_cost_savings": 31000,
        "simple_payback_years": 3.0,
        "npv": 120000,
        "irr": 0.24,
        "global_project_score": 79
      }
    ],
    "recommendation_reason": "Best balance between savings, BACS improvement and payback."
  },
  "meta": {},
  "errors": []
}
```

---

# 8.17 Contrats Reports

## 8.17.1 `POST /api/v1/projects/{project_id}/reports`

### Request

```json
{
  "scenario_id": "1bcd6075-c946-4a77-a43b-5e0dd2dfedab",
  "calculation_run_id": "46604888-f6f2-47a1-90ff-100ea4cbcf3f",
  "report_type": "executive",
  "language": "fr",
  "branding_profile_id": "d9e7efda-e7f0-4302-bc46-83599a4d6c63",
  "include_assumptions": true,
  "include_regulatory_section": true,
  "include_annexes": false
}
```

### Validation

* `scenario_id` obligatoire
* `calculation_run_id` obligatoire
* `report_type` dans `executive|detailed`
* `language` dans `fr|en`

### Response 201

```json
{
  "data": {
    "report_id": "1d0b74bc-c0e4-4815-a3d3-9e6fd5d4c590",
    "generation_status": "generated",
    "report_type": "executive",
    "language": "fr",
    "download_url": "/api/v1/reports/1d0b74bc-c0e4-4815-a3d3-9e6fd5d4c590/download",
    "generated_at": "2026-04-05T11:20:00Z"
  },
  "meta": {},
  "errors": []
}
```

---

## 8.17.2 `GET /api/v1/reports/{report_id}`

### Response 200

```json
{
  "data": {
    "id": "1d0b74bc-c0e4-4815-a3d3-9e6fd5d4c590",
    "project_id": "1b1f44b2-dc2d-45bc-a0b4-52ea68eb5fd7",
    "scenario_id": "1bcd6075-c946-4a77-a43b-5e0dd2dfedab",
    "calculation_run_id": "46604888-f6f2-47a1-90ff-100ea4cbcf3f",
    "report_type": "executive",
    "language": "fr",
    "branding_profile_id": "d9e7efda-e7f0-4302-bc46-83599a4d6c63",
    "generation_status": "generated",
    "file_size_bytes": 542881,
    "download_url": "/api/v1/reports/1d0b74bc-c0e4-4815-a3d3-9e6fd5d4c590/download",
    "generated_at": "2026-04-05T11:20:00Z"
  },
  "meta": {},
  "errors": []
}
```

---

# 8.18 Contrats Admin Config

## 8.18.1 `POST /api/v1/admin/assumption-sets`

### Request

```json
{
  "name": "Default FR v1",
  "country_profile_id": "8cbbe88b-96ce-4fb7-bae0-e69ab5f95bb9",
  "version": "1.0.0",
  "scope": "country_default",
  "heating_model_json": {
    "reference_intensity_kwh_m2": 85
  },
  "cooling_model_json": {
    "reference_intensity_kwh_m2": 18
  },
  "dhw_model_json": {
    "reference_intensity_kwh_room": 2200
  },
  "economic_defaults_json": {
    "discount_rate": 0.06,
    "energy_inflation_rate": 0.03,
    "analysis_period_years": 15
  },
  "bacs_rules_json": {
    "score_to_class": {
      "A": [85, 100],
      "B": [65, 84],
      "C": [40, 64],
      "D": [0, 39]
    }
  },
  "co2_factors_json": {
    "electricity": 0.055,
    "gas": 0.227
  },
  "notes": null,
  "is_active": true
}
```

### Response 201

```json
{
  "data": {
    "id": "d64ce9d4-4468-4453-8c06-f1fda5f4ef8e",
    "name": "Default FR v1",
    "version": "1.0.0",
    "scope": "country_default",
    "is_active": true
  },
  "meta": {},
  "errors": []
}
```

---

# 8.19 Contrats History

## 8.19.1 `GET /api/v1/projects/{project_id}/history`

### Response 200

```json
{
  "data": [
    {
      "id": "f75b2b44-a9a3-428f-a7e8-c5517a3fe327",
      "entity_type": "project",
      "entity_id": "1b1f44b2-dc2d-45bc-a0b4-52ea68eb5fd7",
      "action": "update",
      "user": {
        "id": "9e9fd8cf-8d7f-4c1f-b5d2-83c3cf6e0b8c",
        "name": "Jean Martin"
      },
      "created_at": "2026-04-05T10:40:00Z",
      "summary": "Project updated"
    },
    {
      "id": "1c7ce2f4-cf02-4fd8-adc6-cac906d5df58",
      "entity_type": "calculation_run",
      "entity_id": "46604888-f6f2-47a1-90ff-100ea4cbcf3f",
      "action": "calculate",
      "user": {
        "id": "9e9fd8cf-8d7f-4c1f-b5d2-83c3cf6e0b8c",
        "name": "Jean Martin"
      },
      "created_at": "2026-04-05T11:00:01Z",
      "summary": "Scenario calculated"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 2
  },
  "errors": []
}
```

---

# 8.20 Types normalisés à figer

Je recommande de figer très tôt ces enums.

## `building_type`

* `hotel`
* `aparthotel`
* `residence`
* `other_accommodation`

## `zone_type`

* `guest_rooms`
* `circulation`
* `lobby`
* `restaurant`
* `meeting`
* `technical`
* `spa`
* `pool`
* `other`

## `orientation`

* `north`
* `south`
* `east`
* `west`
* `mixed`

## `system_type`

* `heating`
* `cooling`
* `ventilation`
* `dhw`
* `lighting`
* `auxiliaries`
* `control`

## `bacs_status`

* `present`
* `absent`
* `planned`

## `scenario_type`

* `baseline`
* `improved`
* `target_bacs`
* `custom`

## `report_type`

* `executive`
* `detailed`

## `language`

* `fr`
* `en`

---

# 8.21 Règles de validation transverses

## Règles numériques

* surfaces > 0
* ratios entre 0 et 1
* pourcentages entre 0 et 100 ou 0 et 1 selon convention unique
* puissances > 0 si fournies

## Règles métier

* au moins 1 zone pour calculer
* au moins 1 scénario pour générer un rapport scénario
* un rapport doit pointer vers un `calculation_run` valide
* une solution ciblée `zone` doit avoir `target_zone_id`
* une solution ciblée `system` doit avoir `target_system_id`

## Recommandation forte

Choisir **une convention unique** :

* soit pourcentages stockés en `0.12`
* soit en `12`

Je recommande **0.12** côté API/database.
Le frontend formate en `%`.

---

# 8.22 Contrat minimal OpenAPI à produire ensuite

À partir de ces contrats, l’équipe pourra générer un vrai `openapi.yaml` avec :

* schémas Pydantic,
* exemples,
* enums,
* erreurs standardisées.

Je recommande d’avoir au minimum :

* `schemas/common.py`
* `schemas/auth.py`
* `schemas/projects.py`
* `schemas/wizard.py`
* `schemas/building.py`
* `schemas/zones.py`
* `schemas/systems.py`
* `schemas/bacs.py`
* `schemas/solutions.py`
* `schemas/scenarios.py`
* `schemas/calculations.py`
* `schemas/results.py`
* `schemas/reports.py`
* `schemas/admin.py`

---

# 8.23 Décisions à figer maintenant

Je recommande de figer :

* enveloppe standard `data/meta/errors`
* erreurs structurées avec `code/message/field/details`
* UUID partout
* dates ISO 8601
* ratios en décimaux `0..1`
* enums centralisés
* routes wizard dédiées
* résultats structurés en :

  * `summary`
  * `economic`
  * `messages`
* rapport toujours lié à un `calculation_run`

---

