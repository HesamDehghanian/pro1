from fastapi import APIRouter, Depends, HTTPException
from shared.jwt_utils import decode_jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

@router.get("/dashboard")
def user_dashboard(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = decode_jwt(credentials.credentials)
    if not payload or payload.get("role") != "user":
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"message": f"Welcome to User Dashboard, {payload.get('username')}"}