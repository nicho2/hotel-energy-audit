

# 9. Structure de projet FastAPI complète

## 9.1 Principes d’architecture backend

Je recommande de structurer le backend selon 6 couches :

1. **API layer**
   expose les endpoints REST.

2. **Schemas layer**
   définit les contrats d’entrée/sortie avec Pydantic.

3. **Service layer**
   porte les règles métier applicatives.

4. **Domain / Engine layer**
   porte le moteur de calcul énergétique, BACS, ROI.

5. **Repository layer**
   centralise l’accès à la base.

6. **Persistence layer**
   modèles SQLAlchemy, session DB, migrations.

Cette séparation évite que :

* les routes contiennent de la logique,
* le moteur de calcul dépende du web,
* et les requêtes SQL se dispersent partout.

---

## 9.2 Arborescence globale recommandée

```text
backend/
  app/
    api/
      deps/
      v1/
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

    core/
      config.py
      security.py
      logging.py
      exceptions.py
      constants.py
      i18n.py

    db/
      base.py
      session.py
      models/
        organization.py
        user.py
        branding.py
        project.py
        project_template.py
        building.py
        building_zone.py
        usage_profile.py
        project_usage_override.py
        technical_system.py
        bacs_assessment.py
        bacs_function.py
        solution_catalog.py
        solution_definition.py
        scenario.py
        scenario_solution.py
        calculation_assumption_set.py
        calculation_run.py
        result_summary.py
        result_by_use.py
        result_by_zone.py
        economic_result.py
        generated_report.py
        audit_log.py
        country_profile.py
        climate_zone.py

    repositories/
      base.py
      auth_repository.py
      user_repository.py
      project_repository.py
      building_repository.py
      zone_repository.py
      usage_repository.py
      system_repository.py
      bacs_repository.py
      solution_repository.py
      scenario_repository.py
      calculation_repository.py
      report_repository.py
      admin_repository.py
      audit_repository.py

    schemas/
      common.py
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
      admin.py
      audit.py

    services/
      auth_service.py
      user_service.py
      project_service.py
      wizard_service.py
      building_service.py
      zone_service.py
      usage_service.py
      system_service.py
      bacs_service.py
      solution_service.py
      scenario_service.py
      calculation_service.py
      result_service.py
      report_service.py
      branding_service.py
      admin_service.py
      audit_service.py

    calculation/
      baseline/
        building_baseline.py
        heating.py
        cooling.py
        ventilation.py
        dhw.py
        lighting.py
        auxiliaries.py
      bacs_engine/
        scoring.py
        class_mapper.py
        function_impacts.py
      solution_engine/
        applicability.py
        dependencies.py
        combinator.py
        impacts.py
      economic_engine/
        capex.py
        opex.py
        npv.py
        irr.py
        payback.py
      consolidation/
        aggregator.py
        messages.py
        project_score.py
      snapshots/
        snapshot_builder.py
      engine.py
      types.py

    reporting/
      builders/
        executive_report_builder.py
        detailed_report_builder.py
        comparison_report_builder.py
      templates/
        executive/
        detailed/
        comparison/
      assets/
      pdf/
        html_renderer.py
        pdf_generator.py
      serializers/
        report_context.py

    rules/
      defaults/
      text_rules/
      catalogs/
      climates/
      countries/

    utils/
      dates.py
      numbers.py
      enums.py
      files.py
      json.py

    main.py

  migrations/
    versions/

  tests/
    conftest.py
    fixtures/
    api/
    services/
    calculation/
    reporting/
    repositories/

  scripts/
    seed_countries.py
    seed_climates.py
    seed_bacs_functions.py
    seed_solution_catalog.py
    seed_assumptions.py

  requirements.txt
  alembic.ini
  .env.example
  README.md
  pyproject.toml
```

---

## 9.3 Rôle de chaque dossier

## `api/`

Contient les routeurs FastAPI.

Chaque fichier :

* déclare les endpoints,
* valide les entrées via `schemas`,
* appelle un `service`,
* retourne un objet standardisé.

Les routes doivent rester fines.

---

## `core/`

Contient les briques transverses :

* configuration,
* sécurité,
* exceptions,
* logs,
* constantes,
* internationalisation.

C’est ici qu’on gère :

* les variables d’environnement,
* la config app,
* la stratégie JWT,
* la structure des erreurs API.

---

## `db/`

Contient :

* la session SQLAlchemy,
* le `Base`,
* les modèles ORM.

Le sous-dossier `models/` garde 1 fichier par agrégat principal.

---

## `repositories/`

Chaque repository encapsule :

* les requêtes DB,
* les filtres,
* les jointures,
* la pagination.

Exemple :

* `ProjectRepository.get_by_id()`
* `ScenarioRepository.list_by_project()`
* `CalculationRepository.get_latest_for_scenario()`

Cela évite d’écrire du SQLAlchemy dans tous les services.

---

## `schemas/`

Contient les schémas Pydantic :

* request payloads,
* response DTOs,
* objets imbriqués,
* enums exposés API.

Important :
les schémas API ne doivent pas être confondus avec les modèles ORM.

---

## `services/`

C’est la couche métier applicative.

Exemples :

* `ProjectService.create_project()`
* `WizardService.save_building_step()`
* `BacsService.compute_current_assessment()`
* `ReportService.generate_executive_report()`

C’est ici qu’on orchestre :

* validation métier,
* appels repository,
* appels moteur de calcul,
* traçabilité.

---

## `calculation/`

C’est le cœur différenciant du produit.

Il doit être entièrement découplé de FastAPI.

Il prend :

* des objets d’entrée normalisés,
* des hypothèses,
* des solutions,
* un scénario,

et retourne :

* un résultat de calcul consolidé.

Le moteur doit pouvoir être testé indépendamment du web.

---

## `reporting/`

Contient :

* la préparation du contexte de rapport,
* les templates HTML,
* le moteur HTML → PDF,
* les builders par type de rapport.

L’idée est d’avoir une logique du type :

* `ExecutiveReportBuilder.build_context()`
* `HtmlRenderer.render(template, context)`
* `PdfGenerator.generate(html)`

---

## `rules/`

Contient les données quasi-statiques embarquées ou seedées :

* pays,
* zones climatiques,
* jeux d’hypothèses,
* règles de texte,
* catalogues de départ.

Même si elles finissent en DB, ce dossier est utile pour :

* les seeds,
* le versionnage,
* les fixtures de test.

---

## `tests/`

Découpage recommandé :

* `api/` : tests d’endpoint
* `services/` : logique applicative
* `calculation/` : moteur
* `reporting/` : rapports
* `repositories/` : accès DB

---

# 9.4 Organisation par couche : exemple complet

Prenons le cas `projects`.

## API

`api/v1/projects.py`

* route `POST /projects`
* route `GET /projects`
* route `PATCH /projects/{id}`

## Schema

`schemas/projects.py`

* `ProjectCreate`
* `ProjectUpdate`
* `ProjectResponse`
* `ProjectListItem`

## Repository

`repositories/project_repository.py`

* `create`
* `get_by_id`
* `list_paginated`
* `update`
* `archive`

## Service

`services/project_service.py`

* `create_project`
* `get_project`
* `list_projects`
* `update_project`
* `duplicate_project`

## Model

`db/models/project.py`

Cette répétition par domaine rend le projet lisible.

---

# 9.5 Structure recommandée des modèles ORM

Je recommande SQLAlchemy 2.x avec typing explicite.

## Exemple `project.py`

```python
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, Boolean, Integer, DateTime
from app.db.base import Base
import uuid
from datetime import datetime

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    created_by_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    client_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reference_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")
    wizard_step: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    building_type: Mapped[str] = mapped_column(String(50), nullable=False)
    project_goal: Mapped[str | None] = mapped_column(String(100), nullable=True)

    is_template_based: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    building = relationship("Building", back_populates="project", uselist=False)
    scenarios = relationship("Scenario", back_populates="project")
```

---

# 9.6 Structure recommandée des schémas Pydantic

Je recommande Pydantic v2.

## Exemple `schemas/projects.py`

```python
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Literal

class ProjectCreate(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    client_name: str | None = None
    country_profile_id: UUID
    climate_zone_id: UUID
    building_type: Literal["hotel", "aparthotel", "residence", "other_accommodation"]
    project_goal: str | None = None
    branding_profile_id: UUID | None = None
    template_id: UUID | None = None

class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=255)
    client_name: str | None = None
    project_goal: str | None = None
    wizard_step: int | None = None

class ProjectResponse(BaseModel):
    id: UUID
    name: str
    client_name: str | None
    status: str
    wizard_step: int
    building_type: str
    project_goal: str | None
    created_at: datetime
    updated_at: datetime
```

---

# 9.7 Couche services : conventions

Chaque service doit :

* recevoir une session DB ou unit-of-work,
* appeler les repositories,
* appliquer les règles métier,
* lever des exceptions métier propres.

## Exemple

```python
class ProjectService:
    def __init__(self, project_repo, audit_service):
        self.project_repo = project_repo
        self.audit_service = audit_service

    def create_project(self, payload, current_user):
        project = self.project_repo.create(
            organization_id=current_user.organization_id,
            created_by_user_id=current_user.id,
            **payload.model_dump()
        )
        self.audit_service.log_create("project", project.id, current_user.id)
        return project
```

---

# 9.8 Gestion des exceptions

Je recommande une hiérarchie métier claire.

## Exemple

```python
class AppError(Exception):
    code = "APPLICATION_ERROR"
    message = "Application error"

class NotFoundError(AppError):
    code = "NOT_FOUND"

class ValidationError(AppError):
    code = "VALIDATION_ERROR"

class BusinessRuleError(AppError):
    code = "BUSINESS_RULE_ERROR"

class CalculationNotReadyError(AppError):
    code = "CALCULATION_NOT_READY"
```

Puis un handler FastAPI global transforme cela en JSON standardisé.

---

# 9.9 Dépendances FastAPI

Dans `api/deps/`, je recommande :

* `auth.py`
* `db.py`
* `permissions.py`

## Exemples

* `get_db_session()`
* `get_current_user()`
* `require_org_admin()`
* `require_project_access(project_id)`

Cela garde les routes propres.

---

# 9.10 Structure du moteur de calcul

## `calculation/engine.py`

Point d’entrée unique.

### Rôle

* charge l’entrée de calcul,
* appelle les sous-moteurs,
* consolide,
* retourne un objet résultat complet.

## Exemple de flux

```python
class CalculationEngine:
    def run(self, input_data):
        baseline = self._compute_baseline(input_data)
        bacs = self._compute_bacs(input_data, baseline)
        scenario = self._apply_solutions(input_data, baseline, bacs)
        economic = self._compute_economics(input_data, scenario)
        return self._consolidate(baseline, scenario, bacs, economic)
```

---

## Sous-modules recommandés

### `baseline/`

* calcul usages de base

### `bacs_engine/`

* scoring
* classe
* impacts fonctions

### `solution_engine/`

* applicabilité
* dépendances
* combinaison des gains

### `economic_engine/`

* coûts
* payback
* VAN
* TRI

### `consolidation/`

* agrégation des sorties
* messages automatiques
* score global

### `snapshots/`

* génération des snapshots reproductibles

---

# 9.11 Objets d’entrée/sortie du moteur

Je recommande des dataclasses ou Pydantic internes dédiées.

## Exemple

```python
class CalculationInput(BaseModel):
    project_id: UUID
    scenario_id: UUID
    country_code: str
    climate_zone_code: str
    building: dict
    zones: list[dict]
    systems: list[dict]
    bacs_functions: list[dict]
    selected_solutions: list[dict]
    assumptions: dict
```

## Sortie

```python
class CalculationOutput(BaseModel):
    summary: dict
    by_use: list[dict]
    by_zone: list[dict]
    economic: dict
    bacs: dict
    messages: list[str]
    warnings: list[str]
```

---

# 9.12 Reporting : structure interne

## Builders

* `ExecutiveReportBuilder`
* `DetailedReportBuilder`
* `ComparisonReportBuilder`

## Rôle d’un builder

* charger les données métier,
* préparer un contexte rendu,
* sélectionner les blocs du rapport.

## Pipeline recommandé

```text
ReportService
  -> Builder
    -> ReportContext serializer
      -> HTML renderer
        -> PDF generator
          -> File storage
```

---

## Templates

Je recommande des templates HTML/Jinja :

* plus simples à styliser,
* plus cohérents avec la génération PDF,
* réutilisables pour un aperçu navigateur.

Exemple :

```text
reporting/templates/
  executive/
    base.html
    cover.html
    summary.html
    building.html
    comparison.html
    recommendations.html
  detailed/
    ...
```

---

# 9.13 Gestion des seeds

Il faut des scripts ou commandes pour injecter :

* pays,
* zones climatiques,
* hypothèses V1,
* fonctions BACS,
* catalogue de solutions.

## Exemple

```text
scripts/
  seed_countries.py
  seed_climates.py
  seed_assumptions.py
  seed_bacs_functions.py
  seed_solution_catalog.py
```

Je recommande aussi une commande unique :

```bash
python -m scripts.seed_all
```

---

# 9.14 Gestion de configuration

## `core/config.py`

Je recommande `pydantic-settings`.

### Exemple

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Hotel Energy Audit API"
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REPORT_STORAGE_PATH: str = "./storage/reports"

    class Config:
        env_file = ".env"
```

---

# 9.15 Logging

Le backend doit journaliser :

* login,
* création projet,
* modification données critiques,
* calculs,
* génération rapports,
* erreurs moteur.

Je recommande :

* logs structurés JSON en prod,
* logs lisibles texte en dev.

Fichiers utiles :

* `core/logging.py`

---

# 9.16 Tests à imposer dès le départ

## Niveau 1 — unitaires

* formules de calcul
* mappings BACS
* payback/VAN/TRI
* règles de combinaison des gains

## Niveau 2 — services

* création projet
* duplication
* save wizard
* calcul readiness
* génération rapport

## Niveau 3 — API

* auth
* CRUD projet
* wizard
* calcul
* rapport

## Niveau 4 — snapshot tests

Très utiles pour :

* sorties du moteur,
* structure JSON des résultats,
* rendu HTML du rapport.

---

# 9.17 Migrations DB

Je recommande Alembic.

## Règles

* 1 migration par lot fonctionnel clair
* noms lisibles
* pas de modification manuelle sauvage des tables en environnement partagé

Exemples :

* `001_create_core_org_user_tables`
* `002_create_project_building_tables`
* `003_create_bacs_tables`
* `004_create_scenarios_and_results`

---

# 9.18 Sécurité

## À prévoir dès V1

* hash mot de passe `bcrypt` ou équivalent
* JWT signé
* contrôle organisationnel sur chaque accès
* validation stricte des payloads
* sanitation minimale des champs texte
* contrôle des fichiers branding/logo
* anti path traversal sur les rapports

---

# 9.19 Conventions de code

Je recommande de figer :

* Python 3.12+
* FastAPI
* SQLAlchemy 2.x
* Pydantic v2
* Alembic
* Ruff
* Black
* Mypy léger ou progressif
* Pytest

## Conventions

* fonctions courtes
* services sans SQL direct
* pas de logique métier dans les routes
* pas d’accès DB dans le moteur de calcul
* pas de templates PDF dans les services

---

# 9.20 Fichier `.env.example` recommandé

```env
APP_NAME=Hotel Energy Audit API
ENVIRONMENT=development
API_V1_PREFIX=/api/v1
SECRET_KEY=change-me
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/hotel_audit
ACCESS_TOKEN_EXPIRE_MINUTES=60
REPORT_STORAGE_PATH=./storage/reports
LOG_LEVEL=INFO
DEFAULT_LANGUAGE=fr
```

---

# 9.21 `main.py` recommandé

Le point d’entrée doit :

* initialiser l’app,
* enregistrer les routeurs,
* configurer middleware,
* configurer handlers d’erreurs,
* exposer healthcheck.

## Structure attendue

```python
app = FastAPI(...)
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(project_router, prefix="/api/v1/projects", tags=["projects"])
...
```

Routes utiles :

* `/health`
* `/api/v1/...`

---

# 9.22 Architecture cible de développement

Je recommande ce flux :

### Phase 1

* auth
* organizations
* projects
* wizard
* building/zones/systems

### Phase 2

* BACS
* solutions
* scenarios

### Phase 3

* moteur de calcul
* résultats
* comparaison

### Phase 4

* reporting PDF
* branding
* admin config

### Phase 5

* audit/history
* optimisation
* durcissement

---

# 9.23 Décisions à figer maintenant

Je recommande de figer :

* architecture **modular monolith**
* couches :

  * API
  * schemas
  * services
  * repositories
  * calculation
  * reporting
* moteur de calcul découplé du web
* reporting HTML → PDF
* SQLAlchemy 2 + Pydantic 2
* scripts de seed
* Pytest dès le départ
* Alembic obligatoire
* JWT + RBAC simple

---
