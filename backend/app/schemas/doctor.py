from __future__ import annotations

from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional, Any


class DoctorBase(BaseModel):
    name: str
    specialization: str
    experience_years: Optional[int] = None
    qualification: Optional[str] = None
    hospital_id: str
    consultation_fee: Decimal
    availability: Optional[Any] = None


class DoctorOut(DoctorBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DoctorListOut(BaseModel):
    doctors: list[DoctorOut]
