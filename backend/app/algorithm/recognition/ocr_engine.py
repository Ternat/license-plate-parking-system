import numpy as np
from fast_plate_ocr import LicensePlateRecognizer

class OCREngine:
    def __init__(self):
        self.recognizer = LicensePlateRecognizer("cct-s-v1-global-model")

    def recognize_characters(self, plate_image: np.ndarray):
        if plate_image is None or plate_image.size == 0:
            return "", 0.0
        try:
            result = self.recognizer.run(plate_image, return_confidence=True)
            if not result:
                return "", 0.0

            plate_pred = result[0]
            plate_text = plate_pred.plate.strip().upper()
            if plate_pred.char_probs is not None and len(plate_pred.char_probs) > 0:
                confidence = round(float(np.mean(plate_pred.char_probs)), 4)
            else:
                confidence = 0.0
            return plate_text, confidence
        except Exception as e:
            print(f"OCR error: {e}")
            return "", 0.0

ocr_engine = OCREngine()