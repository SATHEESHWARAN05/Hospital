from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional

from app.database import get_db
from app.models import Hospital, Doctor, Room, Booking
from app.schemas.hospital import HospitalOut, HospitalListOut, HospitalDetailOut, DoctorOut, RoomOut

router = APIRouter()


@router.get("/hospitals", response_model=HospitalListOut)
def list_hospitals(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    city: Optional[str] = None,
    sort_by: Optional[str] = Query("rating", pattern="^(rating|name)$"),
    db: Session = Depends(get_db),
):
    """List all hospitals with optional city filter, paginated."""
    query = db.query(Hospital)

    if city:
        query = query.filter(Hospital.city.ilike(f"%{city}%"))

    total = query.count()

    if sort_by == "rating":
        query = query.order_by(Hospital.rating.desc())
    else:
        query = query.order_by(Hospital.name.asc())

    hospitals = query.offset((page - 1) * page_size).limit(page_size).all()

    return HospitalListOut(
        total=total,
        page=page,
        page_size=page_size,
        hospitals=[HospitalOut.model_validate(h) for h in hospitals],
    )


@router.get("/hospitals/search", response_model=HospitalListOut)
def search_hospitals(
    q: Optional[str] = None,
    city: Optional[str] = None,
    specialization: Optional[str] = None,
    min_rating: Optional[float] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Full-text search across hospital name, city, description.
    Optional filters: city, doctor specialization, minimum rating.
    """
    query = db.query(Hospital)

    if specialization:
        query = query.join(Hospital.doctors).filter(
            Doctor.specialization.ilike(f"%{specialization}%")
        ).distinct()

    if q:
        search_term = f"%{q}%"
        query = query.filter(
            or_(
                Hospital.name.ilike(search_term),
                Hospital.city.ilike(search_term),
                Hospital.description.ilike(search_term),
            )
        )

    if city:
        query = query.filter(Hospital.city.ilike(f"%{city}%"))

    if min_rating is not None:
        query = query.filter(Hospital.rating >= min_rating)

    total = query.count()
    hospitals = query.order_by(Hospital.rating.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    return HospitalListOut(
        total=total,
        page=page,
        page_size=page_size,
        hospitals=[HospitalOut.model_validate(h) for h in hospitals],
    )


@router.get("/hospitals/{hospital_id}", response_model=HospitalDetailOut)
def get_hospital(hospital_id: str, db: Session = Depends(get_db)):
    """Get hospital detail including its doctors and rooms."""
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    doctors = db.query(Doctor).filter(Doctor.hospital_id == hospital_id).all()
    rooms = db.query(Room).filter(Room.hospital_id == hospital_id).all()

    return HospitalDetailOut(
        hospital=HospitalOut.model_validate(hospital),
        doctors=[DoctorOut.model_validate(d) for d in doctors],
        rooms=[RoomOut.model_validate(r) for r in rooms],
    )


@router.get("/hospitals/{hospital_id}/availability", response_model=list[RoomOut])
def hospital_room_availability(
    hospital_id: str,
    date: str = Query(..., description="Check-in date (YYYY-MM-DD)"),
    room_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Return rooms that are NOT booked on the given date."""
    from datetime import date as date_type

    try:
        check_date = date_type.fromisoformat(date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    conflicting_booking_room_ids = (
        db.query(Booking.room_id)
        .filter(
            Booking.room_id.isnot(None),
            Booking.status == "confirmed",
            Booking.check_in_date <= check_date,
            Booking.check_out_date > check_date,
        )
        .subquery()
    )

    query = db.query(Room).filter(
        Room.hospital_id == hospital_id,
        Room.id.notin_(conflicting_booking_room_ids),
    )

    if room_type:
        query = query.filter(Room.room_type == room_type)

    rooms = query.all()
    return [RoomOut.model_validate(r) for r in rooms]
