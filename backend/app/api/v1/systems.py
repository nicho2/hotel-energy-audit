from fastapi import APIRouter

router = APIRouter()


@router.get("/__placeholder__/systems")
def placeholder():
    return {"data": {"module": "systems", "status": "todo"}, "meta": {}, "errors": []}
