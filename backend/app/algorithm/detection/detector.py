from ultralytics import YOLO
import numpy as np
from app.core.config import settings
from app.utils.logger import logger

class PlateDetector:
    def __init__(self):
        self.model_path = settings.DETECT_MODEL_PATH
        logger.info(f"Loading license plate detection model from: {self.model_path}")
        self.model = YOLO(self.model_path)
        self.model.to(settings.DEVICE)

    def detect_plate(self, image: np.ndarray):
        results = self.model(image, conf=settings.DETECT_CONF_THRESHOLD, verbose=False)
        
        if len(results[0].boxes) == 0:
            return None, None, 0.0

        box = results[0].boxes[0]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])

        plate_crop = image[y1:y2, x1:x2]
        return (x1, y1, x2, y2), plate_crop, confidence

plate_detector = PlateDetector()