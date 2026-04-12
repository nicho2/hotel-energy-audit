from sqlalchemy import delete, select

from app.core.security import get_password_hash
from app.db.models.bacs_assessment import BacsAssessment
from app.db.models.bacs_function_definition import BacsFunctionDefinition
from app.db.models.bacs_selected_function import BacsSelectedFunction
from app.db.models.branding_profile import BrandingProfile
from app.db.models.building import Building
from app.db.models.building_zone import BuildingZone
from app.db.models.calculation_run import CalculationRun
from app.db.models.climate_zone import ClimateZone
from app.db.models.country_profile import CountryProfile
from app.db.models.economic_result import EconomicResult
from app.db.models.organization import Organization
from app.db.models.project import Project
from app.db.models.project_template import ProjectTemplate
from app.db.models.result_by_use import ResultByUse
from app.db.models.result_by_zone import ResultByZone
from app.db.models.result_summary import ResultSummary
from app.db.models.scenario import Scenario
from app.db.models.solution_catalog import SolutionCatalog
from app.db.models.solution_definition import SolutionDefinition
from app.db.models.technical_system import TechnicalSystem
from app.db.models.usage_profile import UsageProfile
from app.db.models.user import User
from app.db.session import SessionLocal
try:
    from scripts.demo_seed_data import DEMO_PROJECTS, DEMO_PROJECT_REFERENCE_CODES, ScenarioSeed
except ModuleNotFoundError:
    from demo_seed_data import DEMO_PROJECTS, DEMO_PROJECT_REFERENCE_CODES, ScenarioSeed

DEV_ORGANIZATION_SLUG = "demo-org"
DEV_ORGANIZATION_NAME = "Demo Hospitality Organization"
DEV_USER_EMAIL = "demo@hotel-energy-audit.example.com"
DEV_USER_PASSWORD = "admin1234"
DEMO_SALES_EMAIL = "sales@hotel-energy-audit.example.com"
DEMO_SALES_PASSWORD = "sales1234"
PARTNER_ORGANIZATION_SLUG = "partner-demo-org"
PARTNER_USER_EMAIL = "partner@hotel-energy-audit.example.com"
PARTNER_USER_PASSWORD = "partner1234"

COUNTRY_PROFILE_SEEDS = [
    {
        "country_code": "FR",
        "name_fr": "France",
        "name_en": "France",
        "regulatory_scope": "france_specific",
        "currency_code": "EUR",
        "default_language": "fr",
        "default_discount_rate": 0.06,
        "default_energy_inflation_rate": 0.03,
        "default_analysis_period_years": 15,
    }
]

CLIMATE_ZONE_SEEDS = [
    {
        "country_code": "FR",
        "code": "FR-TEMP",
        "name_fr": "France tempérée",
        "name_en": "Temperate France",
        "heating_severity_index": 1.0,
        "cooling_severity_index": 0.75,
        "solar_exposure_index": 0.85,
        "default_weather_profile_json": {"hdd_base_18": 2200, "cdd_base_26": 120},
        "is_default": True,
    },
    {
        "country_code": "FR",
        "code": "FR-MED",
        "name_fr": "France méditerranéenne",
        "name_en": "Mediterranean France",
        "heating_severity_index": 0.65,
        "cooling_severity_index": 1.25,
        "solar_exposure_index": 1.2,
        "default_weather_profile_json": {"hdd_base_18": 1400, "cdd_base_26": 360},
        "is_default": False,
    },
]

USAGE_PROFILE_SEEDS = [
    {
        "country_code": "FR",
        "code": "FR_HOTEL_GUEST_ROOMS_STANDARD",
        "name_fr": "Chambres hôtel standard",
        "name_en": "Standard hotel guest rooms",
        "building_type": "hotel",
        "zone_type": "guest_rooms",
        "default_occupancy_rate": 0.68,
        "seasonality_profile_json": {
            "jan": 0.55,
            "feb": 0.58,
            "mar": 0.64,
            "apr": 0.70,
            "may": 0.74,
            "jun": 0.78,
            "jul": 0.86,
            "aug": 0.88,
            "sep": 0.76,
            "oct": 0.70,
            "nov": 0.60,
            "dec": 0.57,
        },
        "daily_schedule_json": {"occupied_hours": ["18:00-10:00"], "housekeeping_hours": ["10:00-15:00"]},
        "ecs_intensity_level": "medium",
    },
    {
        "country_code": "FR",
        "code": "FR_HOTEL_LOBBY_STANDARD",
        "name_fr": "Lobby hôtel standard",
        "name_en": "Standard hotel lobby",
        "building_type": "hotel",
        "zone_type": "lobby",
        "default_occupancy_rate": 0.45,
        "seasonality_profile_json": {"annual": 1.0},
        "daily_schedule_json": {"open_hours": ["00:00-24:00"], "peak_hours": ["07:00-10:00", "17:00-21:00"]},
        "ecs_intensity_level": "low",
    },
    {
        "country_code": "FR",
        "code": "FR_HOTEL_RESTAURANT_STANDARD",
        "name_fr": "Restaurant hôtel standard",
        "name_en": "Standard hotel restaurant",
        "building_type": "hotel",
        "zone_type": "restaurant",
        "default_occupancy_rate": 0.50,
        "seasonality_profile_json": {"annual": 1.0},
        "daily_schedule_json": {"service_hours": ["06:00-10:00", "12:00-14:30", "19:00-22:30"]},
        "ecs_intensity_level": "high",
    },
]

BACS_FUNCTION_DEFINITIONS_V1 = [
    {"code": "monitoring.central_supervision", "domain": "monitoring", "name": "Central supervision platform", "description": "A central platform supervises major technical equipment and provides a consolidated view.", "weight": 12.0, "order_index": 1},
    {"code": "monitoring.alarm_reporting", "domain": "monitoring", "name": "Alarm and fault reporting", "description": "The site receives structured alarms for technical faults and can react quickly.", "weight": 8.0, "order_index": 2},
    {"code": "heating.schedule_control", "domain": "heating", "name": "Heating schedules", "description": "Heating operation follows planned schedules adapted to occupancy periods.", "weight": 10.0, "order_index": 1},
    {"code": "heating.zone_control", "domain": "heating", "name": "Heating zone control", "description": "Heating is controlled by zone or functional area instead of one uniform setting.", "weight": 8.0, "order_index": 2},
    {"code": "cooling_ventilation.cooling_schedule", "domain": "cooling_ventilation", "name": "Cooling schedules", "description": "Cooling systems are scheduled according to occupancy and operating periods.", "weight": 10.0, "order_index": 1},
    {"code": "cooling_ventilation.ventilation_demand_control", "domain": "cooling_ventilation", "name": "Demand-controlled ventilation", "description": "Ventilation adapts to occupancy or indoor air quality signals.", "weight": 10.0, "order_index": 2},
    {"code": "dhw.schedule_control", "domain": "dhw", "name": "DHW schedules", "description": "Domestic hot water production is scheduled according to building use patterns.", "weight": 8.0, "order_index": 1},
    {"code": "dhw.temperature_optimization", "domain": "dhw", "name": "DHW temperature optimization", "description": "Hot water production temperature is optimized while keeping service constraints.", "weight": 6.0, "order_index": 2},
    {"code": "lighting.schedule_control", "domain": "lighting", "name": "Lighting schedules", "description": "Lighting follows schedules in common spaces and back-of-house areas.", "weight": 8.0, "order_index": 1},
    {"code": "lighting.occupancy_control", "domain": "lighting", "name": "Occupancy-based lighting control", "description": "Lighting in relevant spaces reacts to presence detection or room status.", "weight": 10.0, "order_index": 2},
]

SOLUTION_CATALOG_SEEDS = [
    {
        "catalog": {
            "name": "Global solution catalog",
            "version": "global-1.0.0",
            "scope": "global",
            "country_code": None,
        },
        "solutions": [
            {
                "code": "ROOM_AUTOMATION_BASIC",
                "name": "Room automation basic",
                "description": "Basic occupancy and setback logic for guest rooms.",
                "family": "bacs",
                "target_scopes": ["zone"],
                "applicable_countries": [],
                "applicable_building_types": ["hotel", "aparthotel", "residence"],
                "applicable_zone_types": ["guest_rooms"],
                "bacs_impact_json": {"domains": ["heating", "cooling"], "target_class_gain": 1},
                "lifetime_years": 10,
                "default_quantity": 1,
                "default_unit": "zone",
                "default_unit_cost": 1800,
                "default_capex": 1800,
                "priority": 10,
                "is_commercial_offer": False,
                "offer_reference": None,
            },
            {
                "code": "LED_RETROFIT_COMMON",
                "name": "LED retrofit common areas",
                "description": "LED retrofit package for circulation and common areas.",
                "family": "lighting",
                "target_scopes": ["zone", "project"],
                "applicable_countries": [],
                "applicable_building_types": ["hotel", "aparthotel", "residence"],
                "applicable_zone_types": ["circulation", "lobby", "restaurant", "meeting"],
                "bacs_impact_json": {"domains": ["lighting"], "target_class_gain": 0},
                "lifetime_years": 12,
                "default_quantity": 1,
                "default_unit": "zone",
                "default_unit_cost": 35,
                "default_capex": 12000,
                "priority": 20,
                "is_commercial_offer": False,
                "offer_reference": None,
            },
            {
                "code": "BOILER_REPLACEMENT_CONDENSING",
                "name": "Condensing boiler replacement",
                "description": "Replace existing heating production with a condensing boiler solution.",
                "family": "hvac",
                "target_scopes": ["system"],
                "applicable_countries": [],
                "applicable_building_types": ["hotel", "aparthotel", "residence"],
                "applicable_zone_types": [],
                "bacs_impact_json": {"domains": ["heating"], "target_class_gain": 0},
                "lifetime_years": 18,
                "default_quantity": 1,
                "default_unit": "system",
                "default_unit_cost": 45000,
                "default_capex": 45000,
                "priority": 30,
                "is_commercial_offer": False,
                "offer_reference": None,
            },
            {
                "code": "HEAT_PUMP_HYBRID",
                "name": "Hybrid heat pump",
                "description": "Hybrid heat pump package for existing accommodation buildings.",
                "family": "hvac",
                "target_scopes": ["system", "project"],
                "applicable_countries": [],
                "applicable_building_types": ["hotel", "aparthotel", "residence"],
                "applicable_zone_types": [],
                "bacs_impact_json": {"domains": ["heating", "cooling"], "target_class_gain": 0},
                "lifetime_years": 16,
                "default_quantity": 1,
                "default_unit": "system",
                "default_unit_cost": 72000,
                "default_capex": 72000,
                "priority": 40,
                "is_commercial_offer": False,
                "offer_reference": None,
            },
        ],
    },
    {
        "catalog": {
            "name": "France solution catalog",
            "version": "fr-1.0.0",
            "scope": "country_specific",
            "country_code": "FR",
        },
        "solutions": [
            {
                "code": "FR_BACS_SUPERVISION_PLUS",
                "name": "BACS supervision plus",
                "description": "France-oriented supervision and alarm reporting package.",
                "family": "bacs",
                "target_scopes": ["project"],
                "applicable_countries": ["FR"],
                "applicable_building_types": ["hotel", "aparthotel"],
                "applicable_zone_types": [],
                "bacs_impact_json": {"domains": ["monitoring"], "target_class_gain": 1},
                "lifetime_years": 12,
                "default_quantity": 1,
                "default_unit": "project",
                "default_unit_cost": 28000,
                "default_capex": 28000,
                "priority": 15,
                "is_commercial_offer": False,
                "offer_reference": None,
            }
        ],
    },
]

ORG_SPECIFIC_SOLUTION_SEED = {
    "catalog": {
        "name": "Demo organization offers",
        "version": "org-demo-1.0.0",
        "scope": "organization_specific",
        "country_code": None,
    },
    "solutions": [
        {
            "code": "DEMO_ROOM_AUTOMATION_OFFER",
            "name": "Demo room automation offer",
            "description": "Organization-specific commercial package for room automation.",
            "family": "bacs",
            "target_scopes": ["zone", "project"],
            "applicable_countries": ["FR"],
            "applicable_building_types": ["hotel"],
            "applicable_zone_types": ["guest_rooms"],
            "bacs_impact_json": {"domains": ["heating", "cooling", "monitoring"], "target_class_gain": 1},
            "lifetime_years": 10,
            "default_quantity": 1,
            "default_unit": "project",
            "default_unit_cost": 24000,
            "default_capex": 24000,
            "priority": 5,
            "is_commercial_offer": True,
            "offer_reference": "DEMO-OFFER-ROOM-AUTO",
        }
    ],
}


def seed_dev_auth_data() -> None:
    with SessionLocal() as db:
        demo_org = _ensure_organization(db, slug=DEV_ORGANIZATION_SLUG, name=DEV_ORGANIZATION_NAME, default_language="fr")
        admin_user = _ensure_user(db, organization=demo_org, email=DEV_USER_EMAIL, password=DEV_USER_PASSWORD, first_name="Demo", last_name="Admin", role="org_admin", preferred_language="fr")
        country_profiles = _ensure_reference_data(db)
        _ensure_project_templates(db, demo_org, admin_user, country_profiles)
        _ensure_bacs_function_definitions(db)
        _ensure_solution_catalogs(db, demo_org)
        db.commit()


def seed_demo_showcase_data() -> None:
    with SessionLocal() as db:
        demo_org = db.scalar(select(Organization).where(Organization.slug == DEV_ORGANIZATION_SLUG))
        admin_user = db.scalar(select(User).where(User.email == DEV_USER_EMAIL))
        if demo_org is None or admin_user is None:
            raise RuntimeError("Run seed_dev_auth_data() before seeding showcase data.")
        default_country = _ensure_reference_data(db)["FR"]
        default_climate = db.scalar(
            select(ClimateZone).where(
                ClimateZone.country_profile_id == default_country.id,
                ClimateZone.is_default.is_(True),
            )
        )
        _ensure_user(db, organization=demo_org, email=DEMO_SALES_EMAIL, password=DEMO_SALES_PASSWORD, first_name="Commercial", last_name="Demo", role="org_member", preferred_language="fr")
        partner_org = _ensure_organization(db, slug=PARTNER_ORGANIZATION_SLUG, name="Partner Demo Organization", default_language="en")
        _ensure_user(db, organization=partner_org, email=PARTNER_USER_EMAIL, password=PARTNER_USER_PASSWORD, first_name="Partner", last_name="Viewer", role="org_admin", preferred_language="en")
        _ensure_branding_profile(db, organization=demo_org, name="Demo default branding", company_name="Hotel Energy Audit Demo", accent_color="#0f766e", logo_text="HEA", contact_email="contact@hotel-energy-audit.example.com", cover_tagline="Executive energy performance summary", footer_note="Prepared for hospitality pre-audit and scenario comparison.", is_default=True)
        _remove_existing_demo_projects(db, demo_org.id)
        definitions_by_code = {definition.code: definition for definition in db.scalars(select(BacsFunctionDefinition)).all()}
        for project_seed in DEMO_PROJECTS:
            _create_demo_project(
                db,
                demo_org,
                admin_user,
                definitions_by_code,
                project_seed,
                country_profile=default_country,
                climate_zone=default_climate,
            )
        db.commit()


def _create_demo_project(db, organization: Organization, admin_user: User, definitions_by_code: dict[str, BacsFunctionDefinition], project_seed, *, country_profile: CountryProfile, climate_zone: ClimateZone | None) -> None:
    project = Project(organization_id=organization.id, created_by_user_id=admin_user.id, name=project_seed.name, client_name=project_seed.client_name, reference_code=project_seed.reference_code, description=project_seed.description, status="ready", wizard_step=10, building_type=project_seed.building_type, project_goal=project_seed.project_goal, country_profile_id=country_profile.id, climate_zone_id=climate_zone.id if climate_zone is not None else None)
    db.add(project)
    db.flush()
    building = Building(project_id=project.id, **project_seed.building)
    db.add(building)
    db.flush()
    zones = [BuildingZone(project_id=project.id, **zone_data) for zone_data in project_seed.zones]
    db.add_all(zones)
    db.flush()
    systems = [TechnicalSystem(project_id=project.id, **system_data) for system_data in project_seed.systems]
    db.add_all(systems)
    db.flush()
    assessment = BacsAssessment(project_id=project.id, version="v1", assessor_name="Demo Seed", notes=f"Demo BACS assessment for {project_seed.name}")
    db.add(assessment)
    db.flush()
    db.add_all([BacsSelectedFunction(assessment_id=assessment.id, function_definition_id=definitions_by_code[code].id) for code in project_seed.bacs_function_codes])
    db.flush()
    for scenario_seed in project_seed.scenarios:
        scenario = Scenario(project_id=project.id, name=scenario_seed.name, description=scenario_seed.description, is_reference=scenario_seed.is_reference)
        db.add(scenario)
        db.flush()
        _create_calculation_run(db, project=project, scenario=scenario, building=building, zones=zones, systems=systems, bacs_function_codes=project_seed.bacs_function_codes, seed=scenario_seed)


def _create_calculation_run(db, *, project: Project, scenario: Scenario, building: Building, zones: list[BuildingZone], systems: list[TechnicalSystem], bacs_function_codes: list[str], seed: ScenarioSeed) -> None:
    run = CalculationRun(project_id=project.id, scenario_id=scenario.id, status="completed", engine_version="demo-seed-v1", input_snapshot={"project_id": str(project.id), "scenario_id": str(scenario.id), "building": _serialize_model(building), "zones": [_serialize_model(zone) for zone in zones], "systems": [_serialize_model(system) for system in systems], "bacs_functions": [{"code": code} for code in bacs_function_codes], "selected_solutions": [], "assumptions": {"engine_version": "demo-seed-v1"}}, messages_json=seed.messages, warnings_json=[], notes="Persisted by demo seed")
    db.add(run)
    db.flush()
    db.add(ResultSummary(calculation_run_id=run.id, baseline_energy_kwh_year=seed.baseline_energy_kwh_year, scenario_energy_kwh_year=seed.scenario_energy_kwh_year, energy_savings_percent=_compute_savings_percent(seed.baseline_energy_kwh_year, seed.scenario_energy_kwh_year), baseline_bacs_class=seed.baseline_bacs_class, scenario_bacs_class=seed.scenario_bacs_class))
    db.add(EconomicResult(calculation_run_id=run.id, total_capex=seed.total_capex, annual_cost_savings=seed.annual_cost_savings, simple_payback_years=seed.simple_payback_years, npv=seed.npv, irr=seed.irr))
    db.add_all(_build_results_by_use(run.id, seed))
    db.add_all(_build_results_by_zone(run.id, zones, seed))


def _build_results_by_use(calculation_run_id, seed: ScenarioSeed) -> list[ResultByUse]:
    shares = {"heating": 0.33, "cooling": 0.14, "ventilation": 0.11, "dhw": 0.24, "lighting": 0.18}
    reduction_factors = {"heating": 1.05, "cooling": 1.1, "ventilation": 0.95, "dhw": 0.9, "lighting": 1.25}
    overall_reduction = _compute_reduction_ratio(seed.baseline_energy_kwh_year, seed.scenario_energy_kwh_year)
    results: list[ResultByUse] = []
    for usage_type, share in shares.items():
        baseline_value = round(seed.baseline_energy_kwh_year * share, 2)
        scenario_value = baseline_value if seed.scenario_energy_kwh_year == seed.baseline_energy_kwh_year else round(baseline_value * (1 - min(overall_reduction * reduction_factors[usage_type], 0.85)), 2)
        results.append(ResultByUse(calculation_run_id=calculation_run_id, usage_type=usage_type, baseline_energy_kwh_year=baseline_value, scenario_energy_kwh_year=scenario_value, energy_savings_percent=_compute_savings_percent(baseline_value, scenario_value)))
    return results


def _build_results_by_zone(calculation_run_id, zones: list[BuildingZone], seed: ScenarioSeed) -> list[ResultByZone]:
    total_area = sum(zone.area_m2 for zone in zones) or float(len(zones) or 1)
    return [ResultByZone(calculation_run_id=calculation_run_id, zone_id=zone.id, zone_name=zone.name, zone_type=zone.zone_type, orientation=zone.orientation, baseline_energy_kwh_year=round(seed.baseline_energy_kwh_year * (zone.area_m2 / total_area), 2), scenario_energy_kwh_year=round((seed.baseline_energy_kwh_year if seed.scenario_energy_kwh_year == seed.baseline_energy_kwh_year else seed.scenario_energy_kwh_year) * (zone.area_m2 / total_area), 2), energy_savings_percent=_compute_savings_percent(round(seed.baseline_energy_kwh_year * (zone.area_m2 / total_area), 2), round((seed.baseline_energy_kwh_year if seed.scenario_energy_kwh_year == seed.baseline_energy_kwh_year else seed.scenario_energy_kwh_year) * (zone.area_m2 / total_area), 2))) for zone in zones]


def _compute_reduction_ratio(baseline: float, scenario: float) -> float:
    if baseline <= 0:
        return 0.0
    return max(min((baseline - scenario) / baseline, 1.0), 0.0)


def _compute_savings_percent(baseline: float, scenario: float) -> float:
    return round(_compute_reduction_ratio(baseline, scenario) * 100, 1)


def _serialize_model(model) -> dict:
    return {key: (str(value) if hasattr(value, "hex") else value) for key, value in vars(model).items() if not key.startswith("_")}


def _ensure_organization(db, *, slug: str, name: str, default_language: str) -> Organization:
    organization = db.scalar(select(Organization).where(Organization.slug == slug))
    if organization is None:
        organization = Organization(name=name, slug=slug, default_language=default_language, is_active=True)
        db.add(organization)
        db.flush()
    else:
        organization.name = name
        organization.default_language = default_language
        organization.is_active = True
    return organization


def _ensure_user(db, *, organization: Organization, email: str, password: str, first_name: str, last_name: str, role: str, preferred_language: str) -> User:
    user = db.scalar(select(User).where(User.email == email))
    password_hash = get_password_hash(password)
    if user is None:
        user = User(organization_id=organization.id, email=email, password_hash=password_hash, first_name=first_name, last_name=last_name, role=role, preferred_language=preferred_language, is_active=True)
        db.add(user)
        db.flush()
    else:
        user.organization_id = organization.id
        user.password_hash = password_hash
        user.first_name = first_name
        user.last_name = last_name
        user.role = role
        user.preferred_language = preferred_language
        user.is_active = True
    return user


def _ensure_branding_profile(db, *, organization: Organization, name: str, company_name: str, accent_color: str, logo_text: str, contact_email: str, cover_tagline: str, footer_note: str, is_default: bool) -> BrandingProfile:
    branding = db.scalar(select(BrandingProfile).where(BrandingProfile.organization_id == organization.id, BrandingProfile.name == name))
    if branding is None:
        branding = BrandingProfile(organization_id=organization.id, name=name, company_name=company_name, accent_color=accent_color, logo_text=logo_text, contact_email=contact_email, cover_tagline=cover_tagline, footer_note=footer_note, is_default=is_default)
        db.add(branding)
        db.flush()
    else:
        branding.company_name = company_name
        branding.accent_color = accent_color
        branding.logo_text = logo_text
        branding.contact_email = contact_email
        branding.cover_tagline = cover_tagline
        branding.footer_note = footer_note
        branding.is_default = is_default
    if is_default:
        for other in db.scalars(select(BrandingProfile).where(BrandingProfile.organization_id == organization.id, BrandingProfile.id != branding.id)).all():
            other.is_default = False
    return branding


def _ensure_reference_data(db) -> dict[str, CountryProfile]:
    countries: dict[str, CountryProfile] = {}
    for data in COUNTRY_PROFILE_SEEDS:
        country = db.scalar(select(CountryProfile).where(CountryProfile.country_code == data["country_code"]))
        if country is None:
            country = CountryProfile(**data)
            db.add(country)
            db.flush()
        else:
            for field, value in data.items():
                setattr(country, field, value)
        countries[country.country_code] = country

    for data in CLIMATE_ZONE_SEEDS:
        country = countries[data["country_code"]]
        climate_data = {key: value for key, value in data.items() if key != "country_code"}
        climate = db.scalar(
            select(ClimateZone).where(
                ClimateZone.country_profile_id == country.id,
                ClimateZone.code == climate_data["code"],
            )
        )
        if climate is None:
            climate = ClimateZone(country_profile_id=country.id, **climate_data)
            db.add(climate)
            db.flush()
        else:
            for field, value in climate_data.items():
                setattr(climate, field, value)

    for data in USAGE_PROFILE_SEEDS:
        country = countries[data["country_code"]]
        usage_data = {key: value for key, value in data.items() if key != "country_code"}
        usage_profile = db.scalar(
            select(UsageProfile).where(
                UsageProfile.country_profile_id == country.id,
                UsageProfile.code == usage_data["code"],
            )
        )
        if usage_profile is None:
            usage_profile = UsageProfile(country_profile_id=country.id, **usage_data)
            db.add(usage_profile)
            db.flush()
        else:
            for field, value in usage_data.items():
                setattr(usage_profile, field, value)
    return countries


def _ensure_project_templates(
    db,
    organization: Organization,
    admin_user: User,
    countries: dict[str, CountryProfile],
) -> ProjectTemplate:
    template = db.scalar(
        select(ProjectTemplate).where(
            ProjectTemplate.organization_id == organization.id,
            ProjectTemplate.name == "Hôtel urbain standard",
        )
    )
    payload = {
        "description": "Template MVP pour hôtel urbain avec zones chambres, lobby et restauration.",
        "building_type": "hotel",
        "country_profile_id": countries["FR"].id,
        "default_payload_json": {
            "wizard_mode": "express",
            "building": {"has_restaurant": True, "main_orientation": "south"},
            "zones": [
                {"zone_type": "guest_rooms", "orientation": "south"},
                {"zone_type": "lobby", "orientation": "north"},
                {"zone_type": "restaurant", "orientation": "east"},
            ],
        },
        "is_active": True,
        "created_by_user_id": admin_user.id,
    }
    if template is None:
        template = ProjectTemplate(
            organization_id=organization.id,
            name="Hôtel urbain standard",
            **payload,
        )
        db.add(template)
        db.flush()
    else:
        for field, value in payload.items():
            setattr(template, field, value)
    return template


def _ensure_bacs_function_definitions(db) -> None:
    for definition_data in BACS_FUNCTION_DEFINITIONS_V1:
        definition = db.scalar(select(BacsFunctionDefinition).where(BacsFunctionDefinition.code == definition_data["code"]))
        if definition is None:
            db.add(BacsFunctionDefinition(version="v1", is_active=True, **definition_data))
        else:
            definition.domain = definition_data["domain"]
            definition.name = definition_data["name"]
            definition.description = definition_data["description"]
            definition.weight = definition_data["weight"]
            definition.order_index = definition_data["order_index"]
            definition.version = "v1"
            definition.is_active = True


def _ensure_solution_catalogs(db, demo_org: Organization) -> None:
    for seed in SOLUTION_CATALOG_SEEDS:
        catalog = _ensure_solution_catalog(db, organization=None, **seed["catalog"])
        for solution_data in seed["solutions"]:
            _ensure_solution_definition(db, catalog, solution_data)

    org_catalog = _ensure_solution_catalog(
        db,
        organization=demo_org,
        **ORG_SPECIFIC_SOLUTION_SEED["catalog"],
    )
    for solution_data in ORG_SPECIFIC_SOLUTION_SEED["solutions"]:
        _ensure_solution_definition(db, org_catalog, solution_data)


def _ensure_solution_catalog(
    db,
    *,
    organization: Organization | None,
    name: str,
    version: str,
    scope: str,
    country_code: str | None,
) -> SolutionCatalog:
    organization_id = organization.id if organization is not None else None
    catalog = db.scalar(
        select(SolutionCatalog).where(
            SolutionCatalog.version == version,
            SolutionCatalog.scope == scope,
            SolutionCatalog.organization_id.is_(organization_id)
            if organization_id is None
            else SolutionCatalog.organization_id == organization_id,
        )
    )
    if catalog is None:
        catalog = SolutionCatalog(
            organization_id=organization_id,
            name=name,
            version=version,
            scope=scope,
            country_code=country_code,
            is_active=True,
        )
        db.add(catalog)
        db.flush()
    else:
        catalog.name = name
        catalog.country_code = country_code
        catalog.is_active = True
    return catalog


def _ensure_solution_definition(db, catalog: SolutionCatalog, data: dict) -> SolutionDefinition:
    solution = db.scalar(select(SolutionDefinition).where(SolutionDefinition.code == data["code"]))
    if solution is None:
        solution = SolutionDefinition(catalog_id=catalog.id, is_active=True, **data)
        db.add(solution)
        db.flush()
    else:
        solution.catalog_id = catalog.id
        for field, value in data.items():
            setattr(solution, field, value)
        solution.is_active = True
    return solution


def _remove_existing_demo_projects(db, organization_id) -> None:
    project_ids = [
        project_id
        for project_id in db.scalars(
            select(Project.id).where(
                Project.organization_id == organization_id,
                Project.reference_code.in_(DEMO_PROJECT_REFERENCE_CODES),
            )
        ).all()
    ]
    if not project_ids:
        return
    db.execute(delete(BacsAssessment).where(BacsAssessment.project_id.in_(project_ids)))
    db.execute(delete(Building).where(Building.project_id.in_(project_ids)))
    db.execute(delete(Project).where(Project.id.in_(project_ids)))
    db.flush()


def main() -> None:
    seed_dev_auth_data()
    seed_demo_showcase_data()
    print("Seed complete.")
    print("Demo credentials:")
    print(f"- admin: {DEV_USER_EMAIL} / {DEV_USER_PASSWORD}")
    print(f"- sales: {DEMO_SALES_EMAIL} / {DEMO_SALES_PASSWORD}")
    print(f"- partner: {PARTNER_USER_EMAIL} / {PARTNER_USER_PASSWORD}")
    print("Demo projects:")
    for project_code in DEMO_PROJECT_REFERENCE_CODES:
        print(f"- {project_code}")


if __name__ == "__main__":
    main()
