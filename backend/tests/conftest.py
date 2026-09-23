import os

import pytest
from fastapi.testclient import TestClient

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app.db.models import Base
from app.db.session import SessionLocal, engine, init_db
from app.main import app
from app.slots.service import seed_slots


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    init_db()
    db = SessionLocal()
    try:
        seed_slots(db)
    finally:
        db.close()

    with TestClient(app) as test_client:
        yield test_client
