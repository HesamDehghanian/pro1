from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from django_app.models import CustomUser, Message
from shared.jwt_utils import decode_jwt

router = APIRouter()
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> CustomUser:
    payload = decode_jwt(credentials.credentials)
    if not payload or payload.get("role") != "user":
        raise HTTPException(status_code=403, detail="Access forbidden")

    try:
        return CustomUser.objects.get(username=payload["username"])
    except CustomUser.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/dashboard")
def user_dashboard(user: CustomUser = Depends(get_current_user)):
    return {
        "message": f"Welcome to User Dashboard, {user.username}",
        "profile": {
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }


@router.post("/send-message")
def send_message(
        user: CustomUser = Depends(get_current_user),
        text: str = Body(...)
):
    Message.objects.create(sender=user, text=text)
    return {"detail": "Message sent successfully"}


@router.put("/profile")
def update_profile(
        user: CustomUser = Depends(get_current_user),
        username: str = Body(...),
        email: str = Body(...)
):
    user.username = username
    user.email = email
    user.save()
    return {"detail": "Profile updated successfully"}


@router.get("/my-messages")
def get_my_messages(user: CustomUser = Depends(get_current_user)):
    messages = Message.objects.filter(sender=user).order_by("-created_at")
    return [
        {
            "text": msg.text,
            "date": msg.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for msg in messages
    ]
