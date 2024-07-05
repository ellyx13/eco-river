from fastapi import APIRouter, UploadFile
from . import schemas
from . import services as video_services

router = APIRouter(
    prefix="/v1",
    tags=["v1/videos"],
)


@router.post("/videos", response_model=schemas.UploadVideoSuccessResponse, 
             responses={413: {"model": schemas.VideoTooLargeResponse}})
async def upload_video(file: UploadFile):
    await video_services.upload_video(file)
    return schemas.UploadVideoSuccessResponse()
