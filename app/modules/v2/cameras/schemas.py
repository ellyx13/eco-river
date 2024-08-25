from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    name: str
    address: str
    username: str
    password: str



class Response(BaseModel):
    id: str = Field(alias="_id")
    name: str
    address: str
    username: str
    password: str
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

