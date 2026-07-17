import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Float, DateTime, Index,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False)
    pincode = Column(String(10), nullable=True)
    phone = Column(String(20), nullable=False)
    email = Column(String(120), nullable=True)
    website = Column(String(200), nullable=True)
    rating = Column(Float, default=0.0)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    doctors = relationship("Doctor", back_populates="hospital", cascade="all, delete-orphan")
    rooms = relationship("Room", back_populates="hospital", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="hospital")
