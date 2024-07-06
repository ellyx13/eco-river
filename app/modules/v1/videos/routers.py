from fastapi import APIRouter, UploadFile
from . import schemas
from . import services as video_services

router = APIRouter(
    prefix="/v1",
    tags=["v1/videos"],
)


@router.post("/videos",  status_code=201, responses={
            201: {'model': schemas.UploadVideoSuccessResponse},
            413: {"model": schemas.VideoTooLargeResponse}})
async def upload_video(file: UploadFile):
    await video_services.upload_video(file)
    return schemas.UploadVideoSuccessResponse()
