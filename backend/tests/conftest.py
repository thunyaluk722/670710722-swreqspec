import os
from importlib import import_module

import pytest
from fastapi.testclient import TestClient

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app.db.models import Base
from app.db.session import SessionLocal, engine
from app.main import app
from app.slots.service import seed_slots

upgrade = import_module('app.db.migrations.001_init').upgrade


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    upgrade(engine)
    db = SessionLocal()
    try:
        seed_slots(db)
    finally:
        db.close()

    with TestClient(app) as test_client:
        yield test_client
