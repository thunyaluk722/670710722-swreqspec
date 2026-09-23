from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.booking.service import create_booking, find_booking
from app.db.session import get_db

router = APIRouter(prefix='')


class BookingRequest(BaseModel):
    hn: str
    slot_id: int


@router.post('/bookings')
def create_booking_route(payload: BookingRequest, db: Session = Depends(get_db)):
    """FR-BKG-04: reserve a slot and return a queue number immediately."""
    result = create_booking(db, payload.hn, payload.slot_id)
    if result['status'] in {'duplicate', 'full'}:
        raise HTTPException(status_code=409, detail=result)
    return result


@router.get('/bookings/{booking_id}')
def get_booking_route(booking_id: int, db: Session = Depends(get_db)):
    """DOM-PDPA-01: read-only detail route for a specific booking record."""
    booking = find_booking(db, booking_id)
    return {
        'booking_id': booking.id,
        'hn': booking.hn,
        'queue_no': booking.queue_no,
        'slot_id': booking.slot_id,
        'booking_date': booking.booking_date.isoformat(),
        'status': booking.status,
    }
