from fastapi import APIRouter

router = APIRouter()


@router.get("/__placeholder__/bacs")
def placeholder():
    return {"data": {"module": "bacs", "status": "todo"}, "meta": {}, "errors": []}
