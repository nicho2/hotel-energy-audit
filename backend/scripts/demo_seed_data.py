from dataclasses import dataclass


@dataclass(frozen=True)
class ScenarioSeed:
    name: str
    description: str
    is_reference: bool
    baseline_energy_kwh_year: float
    scenario_energy_kwh_year: float
    baseline_bacs_class: str
    scenario_bacs_class: str
    total_capex: float
    annual_cost_savings: float
    simple_payback_years: float
    npv: float
    irr: float
    messages: list[str]


@dataclass(frozen=True)
class DemoProjectSeed:
    name: str
    client_name: str
    reference_code: str
    description: str
    building_type: str
    project_goal: str
    building: dict
    zones: list[dict]
    systems: list[dict]
    bacs_function_codes: list[str]
    scenarios: list[ScenarioSeed]


DEMO_PROJECT_REFERENCE_CODES = (
    "DEMO-HOTEL-001",
    "DEMO-APARTHOTEL-001",
    "DEMO-RESIDENCE-001",
)


DEMO_PROJECTS = [
    DemoProjectSeed(
        name="Hotel Lumiere Paris",
        client_name="Groupe Lumiere",
        reference_code="DEMO-HOTEL-001",
        description="Hotel urbain 4 etoiles avec restaurant et salles de reunion.",
        building_type="hotel",
        project_goal="compare_scenarios",
        building={
            "name": "Hotel Lumiere Paris",
            "construction_period": "1990_2005",
            "gross_floor_area_m2": 6200.0,
            "heated_area_m2": 5600.0,
            "cooled_area_m2": 4300.0,
            "number_of_floors": 7,
            "number_of_rooms": 128,
            "main_orientation": "south",
            "compactness_level": "medium",
            "has_restaurant": True,
            "has_meeting_rooms": True,
            "has_spa": False,
            "has_pool": False,
        },
        zones=[
            {"name": "Guest rooms east", "zone_type": "guest_rooms", "orientation": "east", "area_m2": 1800.0, "room_count": 52, "order_index": 1},
            {"name": "Guest rooms west", "zone_type": "guest_rooms", "orientation": "west", "area_m2": 1750.0, "room_count": 50, "order_index": 2},
            {"name": "Lobby and circulation", "zone_type": "circulation", "orientation": "mixed", "area_m2": 980.0, "room_count": 0, "order_index": 3},
            {"name": "Restaurant", "zone_type": "restaurant", "orientation": "south", "area_m2": 920.0, "room_count": 0, "order_index": 4},
            {"name": "Meeting rooms", "zone_type": "meeting", "orientation": "north", "area_m2": 750.0, "room_count": 0, "order_index": 5},
        ],
        systems=[
            {"name": "Main condensing boiler", "system_type": "heating", "energy_source": "natural_gas", "serves": "guest rooms and common areas", "quantity": 2, "year_installed": 2014, "is_primary": True, "order_index": 1},
            {"name": "Air-cooled chiller", "system_type": "cooling", "energy_source": "electricity", "serves": "guest rooms and meeting rooms", "quantity": 1, "year_installed": 2016, "is_primary": True, "order_index": 2},
            {"name": "AHU and kitchen exhaust", "system_type": "ventilation", "energy_source": "electricity", "serves": "restaurant and common spaces", "quantity": 3, "year_installed": 2015, "is_primary": True, "order_index": 3},
            {"name": "DHW production", "system_type": "dhw", "energy_source": "natural_gas", "serves": "rooms and restaurant", "quantity": 1, "year_installed": 2014, "is_primary": True, "order_index": 4},
            {"name": "Common area lighting", "system_type": "lighting", "energy_source": "electricity", "serves": "lobby, corridors and meeting", "quantity": 1, "year_installed": 2018, "is_primary": True, "order_index": 5},
        ],
        bacs_function_codes=[
            "monitoring.central_supervision",
            "monitoring.alarm_reporting",
            "heating.schedule_control",
            "cooling_ventilation.cooling_schedule",
            "lighting.schedule_control",
        ],
        scenarios=[
            ScenarioSeed(
                name="Reference exploitation",
                description="Situation actuelle consolidee.",
                is_reference=True,
                baseline_energy_kwh_year=1420000.0,
                scenario_energy_kwh_year=1420000.0,
                baseline_bacs_class="C",
                scenario_bacs_class="C",
                total_capex=0.0,
                annual_cost_savings=0.0,
                simple_payback_years=0.0,
                npv=0.0,
                irr=0.0,
                messages=["Reference scenario seeded for executive walkthrough."],
            ),
            ScenarioSeed(
                name="Smart rooms + HVAC optimization",
                description="Pilotage chambre, optimisation horaires CVC et LED espaces communs.",
                is_reference=False,
                baseline_energy_kwh_year=1420000.0,
                scenario_energy_kwh_year=1115000.0,
                baseline_bacs_class="C",
                scenario_bacs_class="B",
                total_capex=165000.0,
                annual_cost_savings=46500.0,
                simple_payback_years=3.5,
                npv=182000.0,
                irr=0.24,
                messages=["Demo scenario emphasizes guest-room automation and HVAC scheduling."],
            ),
        ],
    ),
    DemoProjectSeed(
        name="Canal Suites Aparthotel",
        client_name="Urban Stay Collection",
        reference_code="DEMO-APARTHOTEL-001",
        description="Aparthotel long sejour avec occupation variable et espaces partages.",
        building_type="aparthotel",
        project_goal="reduce_energy",
        building={
            "name": "Canal Suites Aparthotel",
            "construction_period": "2005_2015",
            "gross_floor_area_m2": 4100.0,
            "heated_area_m2": 3900.0,
            "cooled_area_m2": 2600.0,
            "number_of_floors": 6,
            "number_of_rooms": 74,
            "main_orientation": "east",
            "compactness_level": "compact",
            "has_restaurant": False,
            "has_meeting_rooms": False,
            "has_spa": False,
            "has_pool": False,
        },
        zones=[
            {"name": "Studios and suites", "zone_type": "guest_rooms", "orientation": "east", "area_m2": 2400.0, "room_count": 74, "order_index": 1},
            {"name": "Lobby coworking", "zone_type": "lobby", "orientation": "south", "area_m2": 520.0, "room_count": 0, "order_index": 2},
            {"name": "Circulation and back office", "zone_type": "circulation", "orientation": "mixed", "area_m2": 680.0, "room_count": 0, "order_index": 3},
            {"name": "Laundry and technical", "zone_type": "technical", "orientation": "north", "area_m2": 500.0, "room_count": 0, "order_index": 4},
        ],
        systems=[
            {"name": "Reversible heat pumps", "system_type": "heating", "energy_source": "electricity", "serves": "studios and suites", "quantity": 74, "year_installed": 2019, "is_primary": True, "order_index": 1},
            {"name": "Balanced ventilation", "system_type": "ventilation", "energy_source": "electricity", "serves": "rooms and common spaces", "quantity": 2, "year_installed": 2018, "is_primary": True, "order_index": 2},
            {"name": "Electric DHW storage", "system_type": "dhw", "energy_source": "electricity", "serves": "all accommodation units", "quantity": 2, "year_installed": 2019, "is_primary": True, "order_index": 3},
            {"name": "LED relamping package", "system_type": "lighting", "energy_source": "electricity", "serves": "common areas", "quantity": 1, "year_installed": 2021, "is_primary": True, "order_index": 4},
        ],
        bacs_function_codes=[
            "monitoring.central_supervision",
            "heating.zone_control",
            "cooling_ventilation.ventilation_demand_control",
            "lighting.occupancy_control",
        ],
        scenarios=[
            ScenarioSeed(
                name="Reference long-stay baseline",
                description="Exploitation actuelle des suites et espaces communs.",
                is_reference=True,
                baseline_energy_kwh_year=860000.0,
                scenario_energy_kwh_year=860000.0,
                baseline_bacs_class="C",
                scenario_bacs_class="C",
                total_capex=0.0,
                annual_cost_savings=0.0,
                simple_payback_years=0.0,
                npv=0.0,
                irr=0.0,
                messages=["Reference aparthotel scenario seeded for long-stay positioning."],
            ),
            ScenarioSeed(
                name="Occupancy-driven comfort control",
                description="Pilotage occupation, ventilation a la demande et relamping cible.",
                is_reference=False,
                baseline_energy_kwh_year=860000.0,
                scenario_energy_kwh_year=684000.0,
                baseline_bacs_class="C",
                scenario_bacs_class="B",
                total_capex=98000.0,
                annual_cost_savings=27600.0,
                simple_payback_years=3.6,
                npv=104000.0,
                irr=0.22,
                messages=["Demo scenario highlights occupancy-based controls for long-stay rooms."],
            ),
        ],
    ),
    DemoProjectSeed(
        name="Residence Azur Seaside",
        client_name="Azure Residences",
        reference_code="DEMO-RESIDENCE-001",
        description="Residence de tourisme avec spa et piscine interieure.",
        building_type="residence",
        project_goal="prepare_investment",
        building={
            "name": "Residence Azur Seaside",
            "construction_period": "1980_1990",
            "gross_floor_area_m2": 5400.0,
            "heated_area_m2": 5000.0,
            "cooled_area_m2": 1400.0,
            "number_of_floors": 4,
            "number_of_rooms": 96,
            "main_orientation": "west",
            "compactness_level": "low",
            "has_restaurant": False,
            "has_meeting_rooms": False,
            "has_spa": True,
            "has_pool": True,
        },
        zones=[
            {"name": "Apartments north wing", "zone_type": "guest_rooms", "orientation": "north", "area_m2": 1700.0, "room_count": 44, "order_index": 1},
            {"name": "Apartments south wing", "zone_type": "guest_rooms", "orientation": "south", "area_m2": 1700.0, "room_count": 52, "order_index": 2},
            {"name": "Reception and circulation", "zone_type": "circulation", "orientation": "mixed", "area_m2": 700.0, "room_count": 0, "order_index": 3},
            {"name": "Spa and pool", "zone_type": "spa", "orientation": "west", "area_m2": 800.0, "room_count": 0, "order_index": 4},
            {"name": "Technical rooms", "zone_type": "technical", "orientation": "mixed", "area_m2": 500.0, "room_count": 0, "order_index": 5},
        ],
        systems=[
            {"name": "Boiler room", "system_type": "heating", "energy_source": "natural_gas", "serves": "apartments and spa", "quantity": 2, "year_installed": 2009, "is_primary": True, "order_index": 1},
            {"name": "Pool dehumidification", "system_type": "ventilation", "energy_source": "electricity", "serves": "pool hall", "quantity": 1, "year_installed": 2012, "is_primary": True, "order_index": 2},
            {"name": "Split cooling in reception", "system_type": "cooling", "energy_source": "electricity", "serves": "reception and admin", "quantity": 3, "year_installed": 2017, "is_primary": True, "order_index": 3},
            {"name": "DHW loop", "system_type": "dhw", "energy_source": "natural_gas", "serves": "apartments and spa", "quantity": 1, "year_installed": 2010, "is_primary": True, "order_index": 4},
            {"name": "Exterior and common lighting", "system_type": "lighting", "energy_source": "electricity", "serves": "common spaces and facades", "quantity": 1, "year_installed": 2016, "is_primary": True, "order_index": 5},
        ],
        bacs_function_codes=[
            "monitoring.central_supervision",
            "monitoring.alarm_reporting",
            "heating.schedule_control",
            "dhw.temperature_optimization",
            "lighting.occupancy_control",
        ],
        scenarios=[
            ScenarioSeed(
                name="Reference residence operation",
                description="Situation actuelle avant travaux et optimisation GTB.",
                is_reference=True,
                baseline_energy_kwh_year=980000.0,
                scenario_energy_kwh_year=980000.0,
                baseline_bacs_class="D",
                scenario_bacs_class="D",
                total_capex=0.0,
                annual_cost_savings=0.0,
                simple_payback_years=0.0,
                npv=0.0,
                irr=0.0,
                messages=["Reference residence scenario seeded for capex planning."],
            ),
            ScenarioSeed(
                name="BACS upgrade + pool optimization",
                description="Modernisation GTB, pilotage spa/piscine et optimisation ECS.",
                is_reference=False,
                baseline_energy_kwh_year=980000.0,
                scenario_energy_kwh_year=812000.0,
                baseline_bacs_class="D",
                scenario_bacs_class="B",
                total_capex=132000.0,
                annual_cost_savings=35200.0,
                simple_payback_years=3.8,
                npv=118000.0,
                irr=0.2,
                messages=["Demo scenario focuses on BACS and pool-side technical optimization."],
            ),
        ],
    ),
]
