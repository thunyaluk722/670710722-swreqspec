from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.slots.service import list_slots, seed_slots

router = APIRouter(prefix='')


@router.get('/slots')
def get_slots(
    date_from: date = Query(..., alias='date_from'),
    package_code: str = Query('basic', alias='package_code'),
    db: Session = Depends(get_db),
):
    """FR-BKG-01: send all available slots for a date range and package selection."""
    seed_slots(db, start_date=date_from)
    return list_slots(db, date_from=date_from, package_code=package_code)
