from fastapi import APIRouter

router = APIRouter()


@router.get("/__placeholder__/results")
def placeholder():
    return {"data": {"module": "results", "status": "todo"}, "meta": {}, "errors": []}
