from datetime import datetime
from typing import Literal, Optional

from core.schemas import ObjectIdStr
from pydantic import BaseModel


class Cameras(BaseModel):
    project_id: ObjectIdStr
    name: str
    address: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    link: Optional[str] = None
    created_at: datetime
    created_by: Optional[ObjectIdStr] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[ObjectIdStr] = None
