from sqlalchemy import Column, Integer, String, Float, DateTime
from app.models.database import Base

class ParkingRecord(Base):
    __tablename__ = "parking_records"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(20), index=True, nullable=False)
    entry_time = Column(DateTime, nullable=False)
    exit_time = Column(DateTime, nullable=True)
    parking_duration = Column(Float, nullable=True)
    parking_fee = Column(Float, nullable=True)
    status = Column(String(10), default="IN")  # IN / OUT
    recognition_confidence = Column(Float, nullable=True)
    exit_confidence = Column(Float, nullable=True)