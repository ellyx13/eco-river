from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from core.schemas import ObjectIdStr

class CreateRequest(BaseModel):
    project_id: ObjectIdStr
    name: str
    address: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    link: Optional[str] = None

class Response(BaseModel):
    id: str = Field(alias="_id")
    project_id: str
    name: str
    address: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    link: Optional[str] = None
    created_at: datetime
    created_by: str


class ListResponse(BaseModel):
    total_items: int
    total_page: int
    records_per_page: int
    results: List[Response]


class EditRequest(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    link: Optional[str] = None


class ObjectResponse(BaseModel):
    name: str
    
    
class ObjectListResponse(BaseModel):
    total_items: int
    total_page: int
    records_per_page: int
    results: List[ObjectResponse]