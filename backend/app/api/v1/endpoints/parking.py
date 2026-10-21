from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.schemas.common import APIResponse
from app.schemas.parking import ParkingEntryResponse, ParkingExitResponse
from app.utils.image_utils import save_uploaded_image
from app.services.parking_service import ParkingService
from app.core.dependencies import verify_token
from app.algorithm.pipeline import lpr_pipeline
from app.utils.logger import logger

router = APIRouter()

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

def is_allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/entry", response_model=APIResponse, summary="Vehicle Entry")
def vehicle_entry(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
):
    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Only JPG/JPEG/PNG images are allowed")

    try:
        image_path = save_uploaded_image(file, "raw")
        result = lpr_pipeline.run_recognition(image_path)
        
        plate_number = result["plate_number"]
        confidence = result["total_confidence"]

        service = ParkingService(db)
        entry_result = service.create_parking_record(plate_number, confidence)

        return APIResponse(code=200, message="Vehicle entry successful", data=ParkingEntryResponse(**entry_result))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/exit", response_model=APIResponse, summary="Vehicle Exit")
def vehicle_exit(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
):
    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Only JPG/JPEG/PNG images are allowed")

    try:
        image_path = save_uploaded_image(file, "raw")
        result = lpr_pipeline.run_recognition(image_path)
        plate_number = result["plate_number"]
        confidence = result["total_confidence"]
        service = ParkingService(db)
        exit_result = service.process_vehicle_exit(plate_number, confidence)

        return APIResponse(code=200, message="Vehicle exit successful", data=ParkingExitResponse(**exit_result))
    except Exception as e:
        logger.error(f"Vehicle exit failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))