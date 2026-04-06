from fastapi import APIRouter

router = APIRouter()


@router.get("/__placeholder__/calculations")
def placeholder():
    return {"data": {"module": "calculations", "status": "todo"}, "meta": {}, "errors": []}
