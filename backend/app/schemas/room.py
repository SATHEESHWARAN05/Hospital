from __future__ import annotations

from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional, Any


class RoomBase(BaseModel):
    hospital_id: str
    room_type: str
    room_number: str
    price_per_day: Decimal
    is_available: bool = True
    amenities: Optional[Any] = None
    description: Optional[str] = None


class RoomOut(RoomBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RoomListOut(BaseModel):
    rooms: list[RoomOut]
