from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.schemas.common import APIResponse
from app.utils.image_utils import save_uploaded_image
from app.core.dependencies import verify_token
from app.algorithm.pipeline import lpr_pipeline
from app.utils.logger import logger

router = APIRouter()

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

def is_allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/run", response_model=APIResponse, summary="End-to-End License Plate Recognition")
def run_recognition(
    file: UploadFile = File(...),
    token_data: dict = Depends(verify_token)
):
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only JPG/JPEG/PNG images are allowed."
        )

    try:
        image_path = save_uploaded_image(file, "raw")
        result = lpr_pipeline.run_recognition(image_path)
        
        return APIResponse(code=200, message="Recognition successful", data=result)
    except Exception as e:
        logger.error(f"Recognition failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))