from fastapi import APIRouter

from app.api.v1.endpoints import (
    assumptions,
    auth,
    bacs,
    branding,
    buildings,
    calculations,
    history,
    projects,
    reports,
    results,
    scenario_management,
    scenarios,
    systems,
    wizard,
    zones,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(branding.router, prefix="/branding", tags=["branding"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(assumptions.router, prefix="/projects", tags=["assumptions"])
api_router.include_router(history.router, prefix="/projects", tags=["history"])
api_router.include_router(wizard.router, prefix="/projects", tags=["wizard"])
api_router.include_router(buildings.router, prefix="/projects", tags=["buildings"])
api_router.include_router(zones.router, prefix="/projects", tags=["zones"])
api_router.include_router(systems.router, prefix="/projects", tags=["systems"])
api_router.include_router(bacs.router, prefix="/projects", tags=["bacs"])
api_router.include_router(scenario_management.router, prefix="/projects", tags=["scenario-management"])
api_router.include_router(scenarios.router, prefix="/projects", tags=["scenarios"])
api_router.include_router(calculations.router, prefix="/projects", tags=["calculations"])
api_router.include_router(results.router, tags=["results"])
api_router.include_router(reports.router, tags=["reports"])
