from fastapi import APIRouter
from modules.v1.healthy import routers as healthy_routers




api_router = APIRouter()

# Healthy
api_router.include_router(healthy_routers.router)
