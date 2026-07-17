import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, Text, ForeignKey, Numeric, DateTime, JSON,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    hospital_id = Column(String(36), ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False)
    room_type = Column(String(50), nullable=False)
    room_number = Column(String(20), nullable=False)
    price_per_day = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, default=True)
    amenities = Column(JSON, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hospital = relationship("Hospital", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")
