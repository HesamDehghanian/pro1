from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastApi_app.routers import user_router, admin_router, superadmin_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, prefix="/user")
app.include_router(admin_router.router, prefix="/admin")
app.include_router(superadmin_router.router, prefix="/superadmin")
