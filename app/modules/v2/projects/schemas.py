from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    name: str
    river_name: str
    ward: str
    district: str
    province: str
    country: str



class Response(BaseModel):
    id: str = Field(alias="_id")
    name: str
    river_name: str
    ward: str
    district: str
    province: str
    country: str
    created_at: datetime
    created_by: str


class ListResponse(BaseModel):
    total_items: int
    total_page: int
    records_per_page: int
    results: List[Response]


class EditRequest(BaseModel):
    name: Optional[str] = None
    river_name: Optional[str] = None
    ward: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None

