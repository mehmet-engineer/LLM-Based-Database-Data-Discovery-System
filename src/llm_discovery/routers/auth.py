from fastapi import APIRouter, Depends
from llm_discovery.core.security import verify_credentials

# create an API router for authentication-related endpoints
router = APIRouter(prefix="/auth", tags=["Authentication"])

# handling GET /auth
@router.get("")
def auth_endpoint(username: str = Depends(verify_credentials)):
    return {"status": "authenticated", "user": username}