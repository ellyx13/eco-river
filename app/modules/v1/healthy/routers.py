from fastapi import APIRouter

router = APIRouter(
    tags=['v1/healthy']
)

@router.get('/v1/ping')
async def pong():
    return {"ping": "pong!"}
