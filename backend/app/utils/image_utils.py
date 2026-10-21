import os
import cv2
from datetime import datetime
from app.core.config import settings

def save_uploaded_image(file, subdir: str) -> str:
    """
    Save uploaded file to specified subdirectory
    :param file: UploadFile object from FastAPI
    :param subdir: Subdirectory name (raw/enhanced/detection/corrected)
    :return: Full path to saved image
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = f"{timestamp}_{file.filename}"
    
    save_dir = os.path.join(settings.UPLOAD_BASE_DIR, subdir)
    os.makedirs(save_dir, exist_ok=True)
    
    save_path = os.path.join(save_dir, filename)
    with open(save_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    return save_path

def save_image(image, save_dir: str, filename: str) -> str:
    """
    Save OpenCV image to specified directory
    :param image: OpenCV image (numpy array)
    :param save_dir: Directory to save image
    :param filename: Filename for saved image
    :return: Full path to saved image
    """
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    cv2.imwrite(save_path, image)
    return save_path