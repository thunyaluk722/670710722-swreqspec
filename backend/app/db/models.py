from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Slot(Base):
    __tablename__ = 'slots'

    id = Column(Integer, primary_key=True, index=True)
    slot_date = Column(Date, nullable=False, index=True)
    start_time = Column(String, nullable=False)
    package_code = Column(String, nullable=False, default='basic')
    capacity = Column(Integer, nullable=False, default=1)
    remaining = Column(Integer, nullable=False, default=1)

    bookings = relationship('Booking', back_populates='slot')


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    hn = Column(String, nullable=False, index=True)
    slot_id = Column(Integer, ForeignKey('slots.id'), nullable=False)
    booking_date = Column(Date, nullable=False)
    queue_no = Column(String, nullable=False)
    status = Column(String, nullable=False, default='confirmed')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    slot = relationship('Slot', back_populates='bookings')


class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    hn = Column(String, nullable=False)
    accessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
