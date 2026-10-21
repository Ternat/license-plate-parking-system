from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    
    PROJECT_NAME: str = "License Plate Recognition Parking System"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./parking.db"
    DETECT_MODEL_PATH: str = "./weights/best.pt"
    DETECT_CONF_THRESHOLD: float = 0.15
    DEVICE: str = "cpu"
    OCR_LANG_LIST: List[str] = ["en"]
    OCR_USE_GPU: bool = False
    OCR_CONF_THRESHOLD: float = 0.1
    FREE_PARKING_HOURS: float = 2.0
    HOURLY_PARKING_FEE: float = 5.0
    UPLOAD_BASE_DIR: str = "./uploads"
    UPLOAD_RAW_DIR: str = "./uploads/raw"
    UPLOAD_ENHANCED_DIR: str = "./uploads/enhanced"
    UPLOAD_DETECTION_DIR: str = "./uploads/detection"
    UPLOAD_CORRECTED_DIR: str = "./uploads/corrected"
    SECRET_KEY: str = "parking-system-2024-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    BRIGHTNESS_LOW_THRESHOLD: int = 80
    BRIGHTNESS_HIGH_THRESHOLD: int = 220
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "123456"

    class Config:
        env_file = ".env"

settings = Settings()