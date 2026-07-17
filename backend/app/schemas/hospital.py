from __future__ import annotations

from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Any


# ── Hospital ──────────────────────────────────────────

class HospitalBase(BaseModel):
    name: str
    address: str
    city: str
    state: str
    pincode: Optional[str] = None
    phone: str
    email: Optional[str] = None
    website: Optional[str] = None
    rating: float = 0.0
    description: Optional[str] = None
    image_url: Optional[str] = None


class HospitalOut(HospitalBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class HospitalListOut(BaseModel):
    total: int
    page: int
    page_size: int
    hospitals: list[HospitalOut]


class HospitalDetailOut(BaseModel):
    hospital: HospitalOut
    doctors: list["DoctorOut"]
    rooms: list["RoomOut"]


# ── Doctor ────────────────────────────────────────────

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


# ── Room ──────────────────────────────────────────────

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


# ── Booking ────────────────────────────────────────────

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
