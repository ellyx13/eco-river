from fastapi import APIRouter
from modules.v1.healthy import routers as healthy_routers
from modules.v1.videos import routers as video_routers




api_router = APIRouter()

# Healthy
api_router.include_router(healthy_routers.router)
api_router.include_router(video_routers.router)
