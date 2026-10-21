from pydantic import BaseModel
from typing import List, Optional

class RecognitionResult(BaseModel):
    """Recognition result data model (English fields)"""
    status: str
    message: str
    image_filename: str
    plate_number: str  
    total_confidence: float
    detection_confidence: float
    ocr_confidence: float
    bounding_box: Optional[List[int]] = None  # [x1, y1, x2, y2]