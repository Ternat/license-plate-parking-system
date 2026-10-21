from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.schemas.common import APIResponse
from app.schemas.parking import ParkingRecordResponse
from app.services.record_service import RecordService
from app.core.dependencies import verify_token
# UK Parking System - Records API
router = APIRouter()

@router.get("/all", response_model=APIResponse, summary="Get All UK Parking Records")
async def get_all_records(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
):
    """
    Get all parking records with pagination (UK Parking System)
    """
    service = RecordService(db)
    records = service.get_all_records(skip=skip, limit=limit)
    total = service.count_all_records()
    return APIResponse(
        code=200,
        message="All parking records retrieved successfully",
        data={
            "items": [ParkingRecordResponse.from_orm(r) for r in records],
            "total": total
        }
    )

@router.get("/by-plate", response_model=APIResponse, summary="Get Records by License Plate")
async def get_records_by_plate(
    plate_number: str = Query(..., description="UK License Plate Number"),
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
):
    """
    Query parking records by vehicle license plate
    """
    service = RecordService(db)
    records = service.get_record_by_plate(plate_number)
    return APIResponse(
        code=200,
        message="Parking records retrieved successfully",
        data=[ParkingRecordResponse.from_orm(r) for r in records]
    )

@router.get("/active", response_model=APIResponse, summary="Get Active Parking Records")
async def get_active_records(
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
):
    """
    Get vehicles currently parked in the lot (Status = IN)
    """
    service = RecordService(db)
    records = service.get_active_records()
    return APIResponse(
        code=200,
        message="Active parking records retrieved successfully",
        data=[ParkingRecordResponse.from_orm(r) for r in records]
    )