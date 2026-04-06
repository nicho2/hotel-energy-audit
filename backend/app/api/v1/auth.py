from fastapi import APIRouter
from app.schemas.auth import LoginRequest

router = APIRouter()


@router.post("/login")
def login(payload: LoginRequest):
    return {
        "data": {
            "access_token": "dev-token",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": {
                "id": "00000000-0000-0000-0000-000000000001",
                "organization_id": "00000000-0000-0000-0000-000000000001",
                "email": payload.email,
                "first_name": "Demo",
                "last_name": "User",
                "role": "org_admin",
                "preferred_language": "fr",
                "is_active": True,
            },
        },
        "meta": {"version": "v1"},
        "errors": [],
    }
