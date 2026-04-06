from fastapi import APIRouter

router = APIRouter()


@router.get("/{project_id}/wizard")
def get_wizard_state(project_id: str):
    return {
        "data": {
            "current_step": 1,
            "steps": [
                {"step": 1, "name": "project", "status": "completed"},
                {"step": 2, "name": "context", "status": "not_started"},
                {"step": 3, "name": "building", "status": "not_started"},
            ],
            "readiness": {"can_calculate": False, "confidence_level": "low"},
        },
        "meta": {},
        "errors": [],
    }
