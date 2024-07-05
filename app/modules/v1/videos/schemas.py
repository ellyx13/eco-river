from pydantic import BaseModel
from typing import Literal


class UploadVideoResponse(BaseModel):
    status: Literal['success', 'failed']
    message: str
    
class UploadVideoSuccessResponse(BaseModel):
    status_code: int = 201
    status: str = 'success'
    message: str = 'Video is being analyzed'

class VideoTooLargeResponse(BaseModel):
    status_code: int = 413
    status: str = 'failed'
    message: str = 'Video too large'