from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import Doctor, Hospital
from app.schemas.doctor import DoctorOut, DoctorListOut

router = APIRouter()


@router.get("/doctors", response_model=DoctorListOut)
def list_doctors(
    hospital_id: Optional[str] = None,
    specialization: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List doctors, optionally filtered by hospital and/or specialization."""
    query = db.query(Doctor)

    if hospital_id:
        query = query.filter(Doctor.hospital_id == hospital_id)

    if specialization:
        query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))

    doctors = query.order_by(Doctor.name.asc()).all()
    return DoctorListOut(doctors=[DoctorOut.model_validate(d) for d in doctors])


@router.get("/doctors/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: str, db: Session = Depends(get_db)):
    """Get a single doctor's detail."""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return DoctorOut.model_validate(doctor)
