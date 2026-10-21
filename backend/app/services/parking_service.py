from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.parking import ParkingRecord
from app.core.config import settings
from app.utils.logger import logger
from app.utils.time_utils import calculate_duration_hours, format_datetime
from typing import Optional, Dict, Any
import math

def _get_pricing() -> dict:
    try:
        from app.api.v1.endpoints.pricing import get_current_pricing
        return get_current_pricing()
    except Exception:
        return {"free_hours": settings.FREE_PARKING_HOURS, "hourly_rate": settings.HOURLY_PARKING_FEE}

class ParkingService:
    """
    Business logic for parking operations (entry, exit, fee calculation)
    Optimized for UK parking standards
    """
    def __init__(self, db: Session):
        self.db = db
        pricing = _get_pricing()
        self.free_hours = pricing["free_hours"]
        self.hourly_rate = pricing["hourly_rate"]

    def create_parking_record(self, plate_number: str, confidence: float) -> Dict[str, Any]:
        """
        Create a new parking record on vehicle entry
        :param plate_number: Recognized UK license plate number
        :param confidence: Recognition confidence score
        :return: Parking entry data
        """
        existing_record = self.db.query(ParkingRecord).filter(
            ParkingRecord.plate_number == plate_number,
            ParkingRecord.status == "IN"
        ).first()

        if existing_record:
            logger.warning(f"Duplicate entry attempt for plate: {plate_number}")
            raise Exception(f"Vehicle {plate_number} is already parked in the lot")

        entry_time = datetime.now(timezone.utc).replace(tzinfo=None)
        
        parking_record = ParkingRecord(
            plate_number=plate_number,
            entry_time=entry_time,
            status="IN",
            recognition_confidence=confidence
        )

        self.db.add(parking_record)
        self.db.commit()
        self.db.refresh(parking_record)

        logger.info(f"Vehicle entered: {plate_number} at {entry_time}")
        return {
            "plate_number": parking_record.plate_number,
            "entry_time": parking_record.entry_time.isoformat(),
            "confidence": confidence
        }

    def process_vehicle_exit(self, plate_number: str, confidence: float) -> Dict[str, Any]:
        """
        Process vehicle exit, calculate duration and fee
        :param plate_number: Recognized UK license plate number
        :param confidence: Recognition confidence score
        :return: Parking exit data with fee
        """
        parking_record = self.db.query(ParkingRecord).filter(
            ParkingRecord.plate_number == plate_number,
            ParkingRecord.status == "IN"
        ).first()

        if not parking_record:
            logger.error(f"No active parking record found for plate: {plate_number}")
            raise Exception(f"No active parking record found for {plate_number}")
            
        exit_time = datetime.now(timezone.utc).replace(tzinfo=None)
        entry_time = parking_record.entry_time

        parking_duration_hours = calculate_duration_hours(entry_time, exit_time)
        
        if parking_duration_hours <= self.free_hours:
            parking_fee = 0.0
        else:
            chargeable_hours = parking_duration_hours - self.free_hours
            paid_hours = math.ceil(chargeable_hours)
            parking_fee = round(paid_hours * self.hourly_rate, 2)

        parking_record.exit_time = exit_time
        parking_record.parking_duration = parking_duration_hours
        parking_record.parking_fee = parking_fee
        parking_record.status = "OUT"
        parking_record.exit_confidence = confidence

        self.db.commit()
        self.db.refresh(parking_record)

        logger.info(f"Vehicle exited: {plate_number}, duration: {parking_duration_hours}h, fee: £{parking_fee}")
        return {
            "plate_number": parking_record.plate_number,
            "entry_time": parking_record.entry_time.isoformat(),
            "exit_time": parking_record.exit_time.isoformat(),
            "parking_duration": parking_record.parking_duration,
            "parking_fee": parking_record.parking_fee,
            "confidence": confidence
        }

    def get_parking_record_by_id(self, record_id: int) -> Optional[ParkingRecord]:
        """Get parking record by ID"""
        return self.db.query(ParkingRecord).filter(ParkingRecord.id == record_id).first()

parking_service = ParkingService