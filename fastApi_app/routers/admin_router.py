from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from shared.jwt_utils import decode_jwt
from django_app.models import CustomUser, Message

router = APIRouter()
security = HTTPBearer()


def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)) -> CustomUser:
    payload = decode_jwt(credentials.credentials)
    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")

    try:
        admin_user = CustomUser.objects.get(username=payload["username"])
        return admin_user
    except CustomUser.DoesNotExist:
        raise HTTPException(status_code=404, detail="Admin user not found")


@router.get("/dashboard")
def admin_dashboard(admin_user: CustomUser = Depends(get_current_admin)):

    users = list(CustomUser.objects.filter(role="user").values("id", "username", "email"))
    messages = Message.objects.select_related("sender").order_by("-created_at")
    msg_data = [

        {
            "from": msg.sender.username,
            "text": msg.text,
            "date": msg.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for msg in messages
    ]

    return {
        "message": f"Welcome to Admin Dashboard, {admin_user.username}",
        "users": users,
        "support_messages": msg_data
    }


@router.put("/profile")
def update_admin_profile(
    admin_user: CustomUser = Depends(get_current_admin),
    username: str = Body(...),
    email: str = Body(...)
):
    admin_user.username = username
    admin_user.email = email
    admin_user.save()
    return {"detail": "Profile updated successfully"}
