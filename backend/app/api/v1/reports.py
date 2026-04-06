from fastapi import APIRouter

router = APIRouter()


@router.get("/__placeholder__/reports")
def placeholder():
    return {"data": {"module": "reports", "status": "todo"}, "meta": {}, "errors": []}
