from __future__ import annotations

from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


class BookingCreate(BaseModel):
    patient_name: str
    patient_phone: str
    patient_email: Optional[str] = None
    hospital_id: str
    doctor_id: Optional[str] = None
    room_id: Optional[str] = None
    booking_type: str
    check_in_date: date
    check_out_date: Optional[date] = None
    notes: Optional[str] = None


class BookingOut(BaseModel):
    id: str
    patient_name: str
    patient_phone: str
    patient_email: Optional[str] = None
    hospital_id: str
    doctor_id: Optional[str] = None
    room_id: Optional[str] = None
    booking_type: str
    check_in_date: date
    check_out_date: Optional[date] = None
    total_price: Decimal
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
