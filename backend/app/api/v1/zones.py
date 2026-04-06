from fastapi import APIRouter

router = APIRouter()


@router.get("/__placeholder__/zones")
def placeholder():
    return {"data": {"module": "zones", "status": "todo"}, "meta": {}, "errors": []}
