# Mermaid Diagrams

## System view
```mermaid
flowchart LR
    U[Users] --> FE[Frontend]
    FE --> API[Backend API]
    API --> DB[(PostgreSQL)]
    API --> CALC[Calculation Engine]
    API --> REP[Reporting Engine]
    REP --> FILES[File Storage]
```

## Delivery dependency view
```mermaid
flowchart TD
    F1[Foundation] --> F2[Auth]
    F2 --> F3[Projects + Wizard]
    F3 --> F4[Building + Zones + Systems]
    F4 --> F5[BACS + Scenarios]
    F5 --> F6[Calculation]
    F6 --> F7[Results + PDF]
    F7 --> F8[Stabilization]
```


# 12. Schéma Mermaid global du système

## 12.1 Vue système globale

Cette vue montre les grands blocs :

* utilisateurs,
* frontend,
* backend,
* moteur de calcul,
* reporting,
* base de données,
* stockage fichiers,
* référentiels.

```mermaid
flowchart LR
    U1[Commercial]
    U2[Exploitant]
    U3[Admin organisation]

    U1 --> FE[Frontend Web App]
    U2 --> FE
    U3 --> FE

    FE --> API[Backend API FastAPI]

    API --> AUTH[Auth & RBAC]
    API --> PROJ[Projects & Wizard]
    API --> BUILD[Building / Zones / Systems]
    API --> BACS[BACS Assessment]
    API --> SCEN[Scenarios & Solutions]
    API --> CALC[Calculation Engine]
    API --> RES[Results & Comparison]
    API --> REP[Reporting Engine]
    API --> ADMIN[Admin Config]
    API --> AUDIT[Audit & History]

    AUTH --> DB[(PostgreSQL)]
    PROJ --> DB
    BUILD --> DB
    BACS --> DB
    SCEN --> DB
    RES --> DB
    ADMIN --> DB
    AUDIT --> DB

    CALC --> DB
    CALC --> RULES[Rules / Assumptions / Catalogs]

    REP --> DB
    REP --> FILES[File Storage]
    FE --> FILES

    RULES --> DB
```

---

## 12.2 Vue backend modulaire

Cette vue détaille le découpage interne du backend.

```mermaid
flowchart TD
    API[API Layer]

    API --> S_AUTH[Auth Service]
    API --> S_USERS[User Service]
    API --> S_ORG[Organization Service]
    API --> S_BRAND[Branding Service]
    API --> S_PROJ[Project Service]
    API --> S_WIZ[Wizard Service]
    API --> S_BUILD[Building Service]
    API --> S_ZONE[Zone Service]
    API --> S_USAGE[Usage Service]
    API --> S_SYS[System Service]
    API --> S_BACS[BACS Service]
    API --> S_SOL[Solution Service]
    API --> S_SCEN[Scenario Service]
    API --> S_CALC[Calculation Service]
    API --> S_RES[Result Service]
    API --> S_REP[Report Service]
    API --> S_ADMIN[Admin Service]
    API --> S_AUDIT[Audit Service]

    S_AUTH --> R_AUTH[Repositories]
    S_USERS --> R_USERS[Repositories]
    S_ORG --> R_ORG[Repositories]
    S_BRAND --> R_BRAND[Repositories]
    S_PROJ --> R_PROJ[Repositories]
    S_WIZ --> R_WIZ[Repositories]
    S_BUILD --> R_BUILD[Repositories]
    S_ZONE --> R_ZONE[Repositories]
    S_USAGE --> R_USAGE[Repositories]
    S_SYS --> R_SYS[Repositories]
    S_BACS --> R_BACS[Repositories]
    S_SOL --> R_SOL[Repositories]
    S_SCEN --> R_SCEN[Repositories]
    S_CALC --> R_CALC[Repositories]
    S_RES --> R_RES[Repositories]
    S_REP --> R_REP[Repositories]
    S_ADMIN --> R_ADMIN[Repositories]
    S_AUDIT --> R_AUDIT[Repositories]

    S_CALC --> ENGINE[Calculation Engine]
    S_REP --> REPORTING[Reporting Engine]

    R_AUTH --> DB[(PostgreSQL)]
    R_USERS --> DB
    R_ORG --> DB
    R_BRAND --> DB
    R_PROJ --> DB
    R_WIZ --> DB
    R_BUILD --> DB
    R_ZONE --> DB
    R_USAGE --> DB
    R_SYS --> DB
    R_BACS --> DB
    R_SOL --> DB
    R_SCEN --> DB
    R_CALC --> DB
    R_RES --> DB
    R_REP --> DB
    R_ADMIN --> DB
    R_AUDIT --> DB

    ENGINE --> RULES[Assumptions / Climate / BACS Rules / Catalogs]
    REPORTING --> FILES[PDF Storage]
```

---

## 12.3 Flux métier principal

Cette vue suit le parcours utilisateur principal du MVP.

```mermaid
flowchart LR
    A[Connexion] --> B[Créer un projet]
    B --> C[Wizard - Contexte]
    C --> D[Wizard - Bâtiment]
    D --> E[Wizard - Zones]
    E --> F[Wizard - Usages]
    F --> G[Wizard - Systèmes]
    G --> H[Wizard - BACS actuel]
    H --> I[Créer un scénario]
    I --> J[Ajouter des solutions]
    J --> K[Vérifier readiness]
    K --> L[Lancer calcul]
    L --> M[Consulter résultats]
    M --> N[Comparer scénarios]
    N --> O[Générer rapport PDF]
    O --> P[Télécharger / partager]
```

---

## 12.4 Flux de calcul détaillé

Cette vue montre le pipeline du moteur de calcul.

```mermaid
flowchart TD
    IN[Input projet/scénario] --> SNAP[Snapshot Builder]

    SNAP --> BASE[Baseline Engine]
    SNAP --> BACS[BACS Engine]
    SNAP --> SOL[Solution Engine]
    SNAP --> ECO[Economic Engine]

    BASE --> CONS[Consolidation Engine]
    BACS --> CONS
    SOL --> CONS
    ECO --> CONS

    CONS --> SUM[Result Summary]
    CONS --> USE[Results by Use]
    CONS --> ZONE[Results by Zone]
    CONS --> BRES[BACS Results]
    CONS --> ERES[Economic Results]
    CONS --> MSG[Automatic Messages]

    SUM --> SAVE[Persist Results]
    USE --> SAVE
    ZONE --> SAVE
    BRES --> SAVE
    ERES --> SAVE
    MSG --> SAVE
```

---

## 12.5 Flux reporting PDF

Cette vue montre comment le rapport est produit.

```mermaid
flowchart TD
    RQ[Generate Report Request] --> LOAD[Load Project / Scenario / Results / Branding]
    LOAD --> BUILD[Report Builder]
    BUILD --> CTX[Report Context]
    CTX --> HTML[HTML Renderer]
    HTML --> PDF[PDF Generator]
    PDF --> STORE[Store File]
    STORE --> META[Save Report Metadata]
    META --> DL[Download URL]
```

---

## 12.6 Vue entités métier principales

Cette vue donne une lecture structurée des principaux objets fonctionnels.

```mermaid
classDiagram
    class Organization {
      +uuid id
      +string name
      +string default_language
    }

    class User {
      +uuid id
      +string email
      +string role
      +bool is_active
    }

    class Project {
      +uuid id
      +string name
      +string status
      +int wizard_step
      +string building_type
    }

    class Building {
      +uuid id
      +float gross_floor_area_m2
      +float heated_area_m2
      +float cooled_area_m2
      +int number_of_rooms
      +string construction_period
    }

    class BuildingZone {
      +uuid id
      +string name
      +string zone_type
      +string orientation
      +float area_m2
      +int room_count
    }

    class TechnicalSystem {
      +uuid id
      +string system_type
      +string technology_type
      +string efficiency_level
    }

    class BacsAssessment {
      +uuid id
      +string estimated_bacs_class
      +string final_bacs_class
      +float confidence_score
    }

    class Scenario {
      +uuid id
      +string name
      +string scenario_type
      +string status
    }

    class ScenarioSolution {
      +uuid id
      +string target_scope
      +float quantity
    }

    class CalculationRun {
      +uuid id
      +string run_status
      +string engine_version
    }

    class ResultSummary {
      +float baseline_energy_kwh_year
      +float scenario_energy_kwh_year
      +float energy_savings_percent
      +string scenario_bacs_class
    }

    class EconomicResult {
      +float total_capex
      +float annual_cost_savings
      +float simple_payback_years
      +float npv
      +float irr
    }

    class GeneratedReport {
      +uuid id
      +string report_type
      +string language
      +string generation_status
    }

    Organization "1" --> "*" User
    Organization "1" --> "*" Project
    Project "1" --> "1" Building
    Project "1" --> "*" Scenario
    Project "1" --> "*" GeneratedReport
    Building "1" --> "*" BuildingZone
    Building "1" --> "*" TechnicalSystem
    Building "1" --> "*" BacsAssessment
    Scenario "1" --> "*" ScenarioSolution
    Scenario "1" --> "*" CalculationRun
    CalculationRun "1" --> "1" ResultSummary
    CalculationRun "1" --> "1" EconomicResult
```

---

## 12.7 Vue des dépendances MVP

Cette vue est utile pour le pilotage du développement.

```mermaid
flowchart TD
    F1[Foundation] --> F2[Auth / Organization]
    F1 --> F3[Projects]
    F3 --> F4[Wizard]
    F4 --> F5[Building / Zones]
    F5 --> F6[Usage / Systems]
    F6 --> F7[BACS]
    F7 --> F8[Solutions / Scenarios]
    F8 --> F9[Calculation Engine]
    F9 --> F10[Results / Comparison]
    F10 --> F11[Reporting PDF]
    F11 --> F12[Stabilization / Audit / Demo]
```

---

## 12.8 Recommandation d’usage de ces schémas

Je vous recommande de conserver ces diagrammes comme base de documentation projet, avec les usages suivants :

* **12.1** pour la vue d’ensemble produit,
* **12.2** pour cadrer l’architecture backend,
* **12.3** pour expliquer le parcours utilisateur,
* **12.4** pour le moteur de calcul,
* **12.5** pour la génération des rapports,
* **12.6** pour la lecture métier / data,
* **12.7** pour le pilotage MVP.

---

