import cv2
import numpy as np
from app.core.config import settings

class ImageEnhancer:
    """
    Image enhancement module for UK license plates
    Optimized for low-light, noise, and low-contrast scenarios common in UK
    """
    def __init__(self):
        pass

    def enhance_image(self, image: np.ndarray) -> np.ndarray:
        """
        Enhance image quality for better LPR performance
        Steps: Bilateral denoising → CLAHE contrast optimization → Brightness adjustment
        :param image: Input OpenCV image (BGR format)
        :return: Enhanced image
        """
        if image is None:
            return None

        denoised = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
        lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l_enhanced = clahe.apply(l)
        lab_enhanced = cv2.merge((l_enhanced, a, b))
        contrast_enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
        hsv = cv2.cvtColor(contrast_enhanced, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        avg_brightness = v.mean()

        if avg_brightness < settings.BRIGHTNESS_LOW_THRESHOLD:
            v = cv2.convertScaleAbs(v, alpha=1.5, beta=30)
        elif avg_brightness > settings.BRIGHTNESS_HIGH_THRESHOLD:
            v = cv2.convertScaleAbs(v, alpha=0.8, beta=-20)

        hsv_enhanced = cv2.merge((h, s, v))
        final_enhanced = cv2.cvtColor(hsv_enhanced, cv2.COLOR_HSV2BGR)

        return final_enhanced

image_enhancer = ImageEnhancer()