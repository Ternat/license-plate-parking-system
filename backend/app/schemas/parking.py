from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ParkingEntryRequest(BaseModel):
    """Request model for vehicle entry (placeholder, uses file upload)"""
    pass

class ParkingEntryResponse(BaseModel):
    """Response model for vehicle entry (English fields)"""
    plate_number: str
    entry_time: str
    confidence: float
    bounding_box: Optional[List[int]] = None

class ParkingExitResponse(BaseModel):
    """Response model for vehicle exit (English fields)"""
    plate_number: str
    entry_time: str
    exit_time: str
    parking_duration: float
    parking_fee: float
    confidence: float

class ParkingRecordResponse(BaseModel):
    """Response model for parking record (English fields)"""
    id: int
    plate_number: str
    entry_time: datetime
    exit_time: Optional[datetime] = None
    parking_duration: Optional[float] = None
    parking_fee: Optional[float] = None
    status: str

    class Config:
        from_attributes = True