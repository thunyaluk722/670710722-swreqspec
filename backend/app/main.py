from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.audit.middleware import audit_middleware
from app.booking.router import router as booking_router
from app.db.session import init_db
from app.slots.router import router as slot_router
from app.slots.service import seed_slots
from app.db.session import SessionLocal

app = FastAPI(title='Booking service')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
def startup() -> None:
    """Initialize PostgreSQL-compatible schema and seed the default slot horizon."""
    init_db()
    db = SessionLocal()
    try:
        seed_slots(db)
    finally:
        db.close()


app.middleware('http')(audit_middleware)
app.include_router(slot_router)
app.include_router(booking_router)
