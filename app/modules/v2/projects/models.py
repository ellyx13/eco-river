from datetime import datetime
from typing import Literal, Optional

from core.schemas import ObjectIdStr
from pydantic import BaseModel


class Projects(BaseModel):
    name: str
    river_name: str
    ward: str
    district: str
    province: str
    country: str
    created_at: datetime
    created_by: Optional[ObjectIdStr] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[ObjectIdStr] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[ObjectIdStr] = None
