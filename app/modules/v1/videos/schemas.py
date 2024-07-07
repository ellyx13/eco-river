from pydantic import BaseModel
from typing import Literal, List


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
    
    
class DetailAnalyzeFakeResponse(BaseModel):
    name: str
    category: str
    environment_score: int
    seconds: int
    
class AnalyzeFakeResponse(BaseModel):
    identifier: str
    total_items: int
    total_environment_score: int
    environmental_pollution_level: str # Low, Medium, High
    results: List[DetailAnalyzeFakeResponse]