from fastapi import APIRouter

router = APIRouter()


@router.get("/__placeholder__/buildings")
def placeholder():
    return {"data": {"module": "buildings", "status": "todo"}, "meta": {}, "errors": []}
