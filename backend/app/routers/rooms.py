from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import Room
from app.schemas.room import RoomOut, RoomListOut

router = APIRouter()


@router.get("/rooms", response_model=RoomListOut)
def list_rooms(
    hospital_id: Optional[str] = None,
    room_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """List rooms, optionally filtered by hospital, room type, and availability."""
    query = db.query(Room)

    if hospital_id:
        query = query.filter(Room.hospital_id == hospital_id)

    if room_type:
        query = query.filter(Room.room_type == room_type)

    if is_available is not None:
        query = query.filter(Room.is_available == is_available)

    rooms = query.order_by(Room.price_per_day.asc()).all()
    return RoomListOut(rooms=[RoomOut.model_validate(r) for r in rooms])


@router.get("/rooms/{room_id}", response_model=RoomOut)
def get_room(room_id: str, db: Session = Depends(get_db)):
    """Get a single room's detail."""
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return RoomOut.model_validate(room)
