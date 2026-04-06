from fastapi import FastAPI
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers

from app.api.v1.auth import router as auth_router
from app.api.v1.projects import router as projects_router
from app.api.v1.wizard import router as wizard_router
from app.api.v1.buildings import router as buildings_router
from app.api.v1.zones import router as zones_router
from app.api.v1.systems import router as systems_router
from app.api.v1.bacs import router as bacs_router
from app.api.v1.scenarios import router as scenarios_router
from app.api.v1.calculations import router as calculations_router
from app.api.v1.results import router as results_router
from app.api.v1.reports import router as reports_router


app = FastAPI(title=settings.app_name)
register_exception_handlers(app)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router, prefix=f"{settings.api_v1_prefix}/auth", tags=["auth"])
app.include_router(projects_router, prefix=f"{settings.api_v1_prefix}/projects", tags=["projects"])
app.include_router(wizard_router, prefix=f"{settings.api_v1_prefix}/projects", tags=["wizard"])
app.include_router(buildings_router, prefix=f"{settings.api_v1_prefix}/projects", tags=["buildings"])
app.include_router(zones_router, prefix=f"{settings.api_v1_prefix}/projects", tags=["zones"])
app.include_router(systems_router, prefix=f"{settings.api_v1_prefix}/projects", tags=["systems"])
app.include_router(bacs_router, prefix=f"{settings.api_v1_prefix}/projects", tags=["bacs"])
app.include_router(scenarios_router, prefix=f"{settings.api_v1_prefix}/projects", tags=["scenarios"])
app.include_router(calculations_router, prefix=f"{settings.api_v1_prefix}/projects", tags=["calculations"])
app.include_router(results_router, prefix=f"{settings.api_v1_prefix}", tags=["results"])
app.include_router(reports_router, prefix=f"{settings.api_v1_prefix}", tags=["reports"])
