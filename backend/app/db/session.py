from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import DATABASE_URL
from app.db.models import Base

if DATABASE_URL.startswith('sqlite'):
    connect_args = {'check_same_thread': False}
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        poolclass=StaticPool,
        future=True,
    )
else:
    engine = create_engine(DATABASE_URL, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    # รองรับ CON-TECH-01 ด้วยการสร้าง schema ผ่าน engine ที่ตั้งค่าไว้
    Base.metadata.create_all(bind=engine)


def get_db():
    # รองรับ CON-TECH-01 โดยจัดการ session ฐานข้อมูลต่อ request
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
