import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Date, Text, ForeignKey, Numeric, DateTime,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_name = Column(String(150), nullable=False)
    patient_phone = Column(String(20), nullable=False)
    patient_email = Column(String(120), nullable=True)
    hospital_id = Column(String(36), ForeignKey("hospitals.id"), nullable=False)
    doctor_id = Column(String(36), ForeignKey("doctors.id"), nullable=True)
    room_id = Column(String(36), ForeignKey("rooms.id"), nullable=True)
    booking_type = Column(String(20), nullable=False)
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=True)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="confirmed")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hospital = relationship("Hospital", back_populates="bookings")
    doctor = relationship("Doctor", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
