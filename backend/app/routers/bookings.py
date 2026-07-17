from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal

from app.database import get_db
from app.models import Booking, Doctor, Room, Hospital
from app.schemas.booking import BookingCreate, BookingOut

router = APIRouter()


def calculate_total_price(
    db: Session,
    booking_type: str,
    doctor_id: str | None,
    room_id: str | None,
    check_in_date,
    check_out_date,
) -> Decimal:
    """Calculate the total price based on booking type."""
    total = Decimal("0.00")

    if booking_type in ("consultation", "both") and doctor_id:
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if doctor:
            total += Decimal(str(doctor.consultation_fee))

    if booking_type in ("admission", "both") and room_id and check_out_date:
        room = db.query(Room).filter(Room.id == room_id).first()
        if room:
            days = (check_out_date - check_in_date).days
            if days < 1:
                days = 1
            total += Decimal(str(room.price_per_day)) * days

    return total


@router.post("/bookings", response_model=BookingOut, status_code=201)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking with auto-calculated price."""
    # Validate hospital exists
    hospital = db.query(Hospital).filter(Hospital.id == payload.hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    # Validate doctor if provided
    if payload.doctor_id:
        doctor = db.query(Doctor).filter(Doctor.id == payload.doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        if str(doctor.hospital_id) != str(payload.hospital_id):
            raise HTTPException(status_code=400, detail="Doctor does not belong to this hospital")

    # Validate room if provided
    if payload.room_id:
        room = db.query(Room).filter(Room.id == payload.room_id).first()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        if str(room.hospital_id) != str(payload.hospital_id):
            raise HTTPException(status_code=400, detail="Room does not belong to this hospital")

    # Validate booking type
    if payload.booking_type not in ("consultation", "admission", "both"):
        raise HTTPException(status_code=400, detail="booking_type must be: consultation, admission, or both")

    # Validate dates for admission
    if payload.booking_type in ("admission", "both") and not payload.check_out_date:
        raise HTTPException(status_code=400, detail="check_out_date is required for admission/both")

    if payload.check_out_date and payload.check_out_date <= payload.check_in_date:
        raise HTTPException(status_code=400, detail="check_out_date must be after check_in_date")

    # Check room availability (no overlapping confirmed bookings)
    if payload.room_id:
        conflicting = (
            db.query(Booking)
            .filter(
                Booking.room_id == payload.room_id,
                Booking.status == "confirmed",
                Booking.check_in_date < payload.check_out_date,
                Booking.check_out_date > payload.check_in_date,
            )
            .first()
        )
        if conflicting:
            raise HTTPException(status_code=409, detail="Room is already booked for the selected dates")

    # Calculate price
    total_price = calculate_total_price(
        db,
        payload.booking_type,
        payload.doctor_id,
        payload.room_id,
        payload.check_in_date,
        payload.check_out_date,
    )

    booking = Booking(
        patient_name=payload.patient_name,
        patient_phone=payload.patient_phone,
        patient_email=payload.patient_email,
        hospital_id=payload.hospital_id,
        doctor_id=payload.doctor_id,
        room_id=payload.room_id,
        booking_type=payload.booking_type,
        check_in_date=payload.check_in_date,
        check_out_date=payload.check_out_date,
        total_price=total_price,
        status="confirmed",
        notes=payload.notes,
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return BookingOut.model_validate(booking)


@router.get("/bookings/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: str, db: Session = Depends(get_db)):
    """Get a booking by ID."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return BookingOut.model_validate(booking)


@router.patch("/bookings/{booking_id}/cancel", response_model=BookingOut)
def cancel_booking(booking_id: str, db: Session = Depends(get_db)):
    """Cancel a booking."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail="Booking is already cancelled")

    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    return BookingOut.model_validate(booking)
