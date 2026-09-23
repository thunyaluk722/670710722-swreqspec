from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.db.models import Slot

DEFAULT_TIMES = ['09:00', '10:45', '13:30']


def seed_slots(db: Session, start_date: date | None = None, package_code: str = 'basic') -> list[Slot]:
    """FR-BKG-01: create a 30-day window of available slots before the UI loads."""
    start_date = start_date or date.today()
    if db.query(Slot).count() > 0:
        return db.query(Slot).all()

    slots: list[Slot] = []
    for offset in range(30):
        current_date = start_date + timedelta(days=offset)
        for time_value in DEFAULT_TIMES:
            slot = Slot(
                slot_date=current_date,
                start_time=time_value,
                package_code=package_code,
                capacity=1,
                remaining=1,
            )
            db.add(slot)
            slots.append(slot)
    db.commit()
    for slot in slots:
        db.refresh(slot)
    return slots


def list_slots(db: Session, date_from: date, package_code: str = 'basic') -> list[dict]:
    query = db.query(Slot).filter(Slot.slot_date >= date_from, Slot.package_code == package_code)
    slots = query.order_by(Slot.slot_date, Slot.start_time).all()
    return [
        {
            'id': slot.id,
            'date': slot.slot_date.isoformat(),
            'slot_date': slot.slot_date.isoformat(),
            'start_time': slot.start_time,
            'package_code': slot.package_code,
            'capacity': slot.capacity,
            'remaining': slot.remaining,
        }
        for slot in slots
    ]
