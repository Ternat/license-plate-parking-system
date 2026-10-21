import cv2
import os
from app.core.config import settings
from app.core.exceptions import PlateDetectionError
from app.algorithm.enhancement.enhancer import image_enhancer
from app.algorithm.detection.detector import plate_detector
from app.algorithm.correction.perspective import perspective_corrector
from app.algorithm.recognition.ocr_engine import ocr_engine
from app.utils.image_utils import save_image
from app.utils.logger import logger

class LPRPipeline:
    """
    End-to-End English License Plate Recognition Pipeline
    adapt fast-plate-ocr + Perspective Correction
    """
    def __init__(self):
        logger.info("Initializing LPR Pipeline...")

    def run_recognition(self, image_path: str, save_intermediate: bool = True) -> dict:
        logger.info(f"Starting recognition for image: {os.path.basename(image_path)}")
        image_filename = os.path.basename(image_path)
        image = cv2.imread(image_path)
        if image is None:
            logger.error("Failed to read input image")
            return {
                "status": "error",
                "message": "Failed to read input image",
                "plate_number": "",
                "total_confidence": 0.0,
                "detection_confidence": 0.0,
                "ocr_confidence": 0.0
            }

        logger.info("Running image enhancement...")
        enhanced_image = image_enhancer.enhance_image(image)
        if save_intermediate:
            save_image(enhanced_image, settings.UPLOAD_ENHANCED_DIR, image_filename)
            
        logger.info("Running license plate detection...")
        bbox, plate_crop, detection_confidence = plate_detector.detect_plate(enhanced_image)
        
        if save_intermediate and bbox is not None:
            detection_viz = enhanced_image.copy()
            x1, y1, x2, y2 = bbox
            cv2.rectangle(detection_viz, (x1, y1), (x2, y2), (0, 255, 0), 3)
            save_image(detection_viz, settings.UPLOAD_DETECTION_DIR, image_filename)

        if plate_crop is None or plate_crop.size == 0:
            logger.warning("No license plate detected")
            raise PlateDetectionError("No license plate detected in the image")
        logger.info(f"Plate detected with confidence: {detection_confidence:.3f}")


        logger.info("Running perspective correction for tilted plate...")
        corrected_plate = perspective_corrector.correct_perspective(plate_crop)
        if save_intermediate:
            save_image(corrected_plate, settings.UPLOAD_CORRECTED_DIR, image_filename)
            logger.info(f"Corrected plate saved to {settings.UPLOAD_CORRECTED_DIR}/{image_filename}")
        logger.info("Running OCR character recognition...")
        plate_number, ocr_confidence = ocr_engine.recognize_characters(corrected_plate)
        
        if not plate_number:
            logger.warning("Failed to recognize plate characters")
            plate_number = "UNRECOGNIZED"
            ocr_confidence = 0.0

        logger.info(f"Plate recognized: {plate_number} (confidence: {ocr_confidence:.3f})")
        total_confidence = round(detection_confidence * ocr_confidence, 3)

        result = {
            "status": "success",
            "message": "Recognition completed successfully",
            "image_filename": image_filename,
            "plate_number": plate_number,
            "total_confidence": total_confidence,
            "detection_confidence": round(detection_confidence, 3),
            "ocr_confidence": round(ocr_confidence, 3),
            "bounding_box": bbox
        }

        logger.info(f"Recognition completed for {image_filename}")
        return result

lpr_pipeline = LPRPipeline()