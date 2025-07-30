import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProject7.settings")

import django
django.setup()

from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model

from django_app.models import CustomUser

# مدل کاربری
User = get_user_model()

# تنظیمات JWT
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 3

# اپ FastAPI
app = FastAPI()

# CORS آزاد
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ساخت توکن JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# لاگین
@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = authenticate(username=user.username, password=password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }

    token = create_access_token(data=payload)
    return {"access_token": token, "user": payload}

# بررسی توکن
security = HTTPBearer()

def decode_jwt(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return None

# دریافت اطلاعات کاربر
@app.get("/me")
def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user": payload}

@app.post("/signup")
def signup(
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...)
):
    if CustomUser.objects.filter(email=email).exists():
        raise HTTPException(status_code=400, detail="Email already registered")

    if CustomUser.objects.filter(username=username).exists():
        raise HTTPException(status_code=400, detail="Username already taken")

    user = CustomUser.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    user.role = "user"
    user.save()

    payload = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }

    token = create_access_token(data=payload)
    return {"access_token": token, "user": payload}
