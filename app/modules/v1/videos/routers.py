from fastapi import APIRouter, UploadFile
from . import schemas
from . import services as video_services

router = APIRouter(
    prefix="/v1",
    tags=["v1/videos"],
)


@router.post("/videos/{identifier}",  status_code=201, responses={
            201: {'model': schemas.UploadVideoSuccessResponse},
            413: {"model": schemas.VideoTooLargeResponse}})
async def upload_video(identifier: str, file: UploadFile):
    await video_services.upload_video(identifier, file)
    return schemas.UploadVideoSuccessResponse()


@router.post("/videos/callback/webhook/fake",  status_code=201, responses={
            201: {'model': schemas.AnalyzeFakeResponse}})
async def generate_fake_webhook(identifier: str, url_callback: str):
    results = await video_services.generate_fake_webhook(identifier, url_callback)
    return schemas.AnalyzeFakeResponse(**results)