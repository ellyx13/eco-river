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
    status_code: int = 413
    status: str = 'failed'
    message: str = 'Video too large'
    
    
class DetailAnalyzeResponse(BaseModel):
    name: str
    category: str
    environment_score: int
    seconds: int
    
class AnalyzeResponse(BaseModel):
    id: str = Field(alias='_id')
    status: str
    total_items: Optional[int] = None
    total_environment_score: Optional[int] = None
    environmental_pollution_level: Optional[str] = None # Low, Medium, High
    results: Optional[List[DetailAnalyzeResponse]] = None