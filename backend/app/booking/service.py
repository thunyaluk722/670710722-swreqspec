from __future__ import annotations

from datetime import date, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Booking, Slot
from app.notify.queue import queue_notification


def _time_to_minutes(value: str) -> int:
    hour, minute = map(int, value.split(':'))
    return hour * 60 + minute


def get_existing_booking_for_hn(db: Session, hn: str, slot_date: date) -> Booking | None:
    return (
        db.query(Booking)
        .join(Slot)
        .filter(Booking.hn == hn, Slot.slot_date == slot_date, Booking.status == 'confirmed')
        .order_by(Booking.created_at.desc())
        .first()
    )


def _build_alternatives(db: Session, slot: Slot) -> list[dict]:
    candidates = (
        db.query(Slot)
        .filter(
            Slot.package_code == slot.package_code,
            Slot.slot_date.in_([slot.slot_date, slot.slot_date + timedelta(days=1)]),
            Slot.remaining > 0,
            Slot.id != slot.id,
        )
        .order_by(Slot.slot_date, Slot.start_time)
        .all()
    )
    result = []
    for candidate in candidates:
        if len(result) >= 3:
            break
        result.append(
            {
                'id': candidate.id,
                'date': candidate.slot_date.isoformat(),
                'start_time': candidate.start_time,
                'remaining': candidate.remaining,
            }
        )
    return result


def create_booking(db: Session, hn: str, slot_id: int) -> dict:
    """FR-BKG-02 / FR-BKG-04: enforce one booking per patient per day and create a queue reference."""
    slot = db.query(Slot).filter(Slot.id == slot_id).first()
    if slot is None:
        raise HTTPException(status_code=404, detail='slot not found')

    duplicate = get_existing_booking_for_hn(db, hn, slot.slot_date)
    if duplicate:
        return {
            'status': 'duplicate',
            'message': 'มีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน',
            'queue_no': duplicate.queue_no,
            'existing_booking_id': duplicate.id,
        }

    if slot.remaining <= 0:
        return {
            'status': 'full',
            'message': 'ช่วงเวลาเต็ม',
            'alternatives': _build_alternatives(db, slot),
        }

    booking = Booking(
        hn=hn,
        slot_id=slot.id,
        booking_date=slot.slot_date,
        queue_no=f'Q-{datetime.utcnow().strftime("%d%H%M")}-{slot.id}',
        status='confirmed',
    )
    slot.remaining = max(slot.remaining - 1, 0)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    queue_notification(booking.id, hn)
    return {
        'status': 'created',
        'booking_id': booking.id,
        'hn': hn,
        'queue_no': booking.queue_no,
        'slot': {
            'id': slot.id,
            'date': slot.slot_date.isoformat(),
            'start_time': slot.start_time,
            'remaining': slot.remaining,
        },
        'notification_status': 'queued',
    }


def find_booking(db: Session, booking_id: int) -> Booking:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=404, detail='booking not found')
    return booking
