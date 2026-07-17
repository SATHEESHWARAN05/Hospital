import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, ForeignKey, Numeric, DateTime, JSON,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(150), nullable=False)
    specialization = Column(String(100), nullable=False, index=True)
    experience_years = Column(Integer, nullable=True)
    qualification = Column(String(200), nullable=True)
    hospital_id = Column(String(36), ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    consultation_fee = Column(Numeric(10, 2), nullable=False)
    availability = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hospital = relationship("Hospital", back_populates="doctors")
    bookings = relationship("Booking", back_populates="doctor")
