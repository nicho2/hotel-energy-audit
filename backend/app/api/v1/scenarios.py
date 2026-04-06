from fastapi import APIRouter

router = APIRouter()


@router.get("/__placeholder__/scenarios")
def placeholder():
    return {"data": {"module": "scenarios", "status": "todo"}, "meta": {}, "errors": []}
