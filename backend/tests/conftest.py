import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.database import Base
from app.models.parking import ParkingRecord  # noqa: F401  (registers the table)
from app.services.parking_service import ParkingService


@pytest.fixture
def db_session():
    """In-memory SQLite session, isolated per test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture
def service(db_session):
    """ParkingService with deterministic pricing: 2 free hours, 5.0/hour."""
    svc = ParkingService(db_session)
    svc.free_hours = 2.0
    svc.hourly_rate = 5.0
    return svc
