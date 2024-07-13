from pydantic import BaseModel, Field
from typing import Literal, List, Optional


class UploadVideoResponse(BaseModel):
    status: Literal['success', 'failed']
    message: str
    
class UploadVideoSuccessResponse(BaseModel):
    id: str = Field(alias='_id')
    status: str = 'success'
    message: str = 'Video is being analyzed'

class NotYetAnalyzedResponse(BaseModel):
    id: str = Field(alias='_id')
    status: str = 'processing'
    
class VideoTooLargeResponse(BaseModel):
    detail: str = 'File size is too big. Limit file is 50 MB.'
    
class VideoTypeNotSupportedResponse(BaseModel):
    detail: str = 'Upload file type are not supported. Please upload the file type .avi, .mp4, .mpeg, .webm.'
    
    
class DetailAnalyzeResponse(BaseModel):
    name: str
    category: str
    environment_score: int
    seconds: int
    boxes: List[float]
    
class AnalyzeResponse(BaseModel):
    id: str = Field(alias='_id')
    status: str
    total_items: Optional[int] = None
    total_environment_score: Optional[int] = None
    environmental_pollution_level: Optional[str] = None # Low, Medium, High
    results: Optional[List[DetailAnalyzeResponse]] = None