from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.reservation import Reservation
from app.models.table import Table
from app.database import get_session
from typing import List
from datetime import datetime, timedelta

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("/", response_model=List[Reservation])
def get_reservations(session: Session = Depends(get_session)):
    return session.exec(select(Reservation)).all()


@router.post("/", response_model=Reservation)
def create_reservation(reservation: Reservation, session: Session = Depends(get_session)):
    # Проверка, существует ли стол
    table = session.get(Table, reservation.table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    # Вычисляем окончание новой брони
    new_start = datetime.strptime(new_start, "%Y-%m-%dT%H:%M:%S")
    new_start = reservation.reservation_time
    new_end = new_start + timedelta(minutes=reservation.duration_minutes)

    # Проверка на пересечение с другими бронями
    stmt = select(Reservation).where(Reservation.table_id == reservation.table_id)
    existing_reservations = session.exec(stmt).all()

    for existing in existing_reservations:
        existing_start = existing.reservation_time
        existing_end = existing_start + timedelta(minutes=existing.duration_minutes)

        if (new_start < existing_end) and (existing_start < new_end):
            raise HTTPException(
                status_code=400,
                detail=f"Table {reservation.table_id} is already reserved for this time",
            )

    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return reservation


@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, session: Session = Depends(get_session)):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    session.delete(reservation)
    session.commit()
    return {"ok": True}
