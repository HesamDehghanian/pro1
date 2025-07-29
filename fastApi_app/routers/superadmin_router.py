from fastapi import APIRouter, Depends, HTTPException
from shared.jwt_utils import decode_jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

@router.get("/dashboard")
def superadmin_dashboard(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = decode_jwt(credentials.credentials)
    if not payload or payload.get("role") != "superadmin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"message": f"Welcome to SuperAdmin Dashboard, {payload.get('username')}"}
