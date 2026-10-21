from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.parking import ParkingRecord
from typing import List, Optional
from app.utils.logger import logger

class RecordService:
    """
    Business logic for parking record management (English function names)
    Handles querying, filtering, and exporting records
    """
    def __init__(self, db: Session):
        self.db = db

    def get_all_records(self, skip: int = 0, limit: int = 100) -> List[ParkingRecord]:
        """
        Get all parking records with pagination
        :param skip: Number of records to skip
        :param limit: Maximum number of records to return
        :return: List of parking records
        """
        logger.info(f"Fetching parking records: skip={skip}, limit={limit}")
        return self.db.query(ParkingRecord).order_by(desc(ParkingRecord.entry_time)).offset(skip).limit(limit).all()

    def count_all_records(self) -> int:
        """Return total number of parking records"""
        return self.db.query(ParkingRecord).count()

    def get_record_by_plate(self, plate_number: str) -> List[ParkingRecord]:
        """
        Get parking records by plate number
        :param plate_number: Plate number to filter
        :return: List of matching parking records
        """
        logger.info(f"Fetching records for plate: {plate_number}")
        return self.db.query(ParkingRecord).filter(
            ParkingRecord.plate_number == plate_number
        ).order_by(desc(ParkingRecord.entry_time)).all()

    def get_active_records(self) -> List[ParkingRecord]:
        """
        Get all active parking records (vehicles currently in parking lot)
        :return: List of active parking records
        """
        logger.info("Fetching active parking records")
        return self.db.query(ParkingRecord).filter(
            ParkingRecord.status == "IN"
        ).order_by(desc(ParkingRecord.entry_time)).all()
record_service = RecordService