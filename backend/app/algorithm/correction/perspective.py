import cv2
import numpy as np

class PerspectiveCorrector:
    """
    Perspective correction module for tilted UK license plates
    Common in UK parking scenarios with angled camera positions
    """
    def __init__(self):
        pass

    def correct_perspective(self, plate_image: np.ndarray) -> np.ndarray:
        """
        Correct perspective distortion for tilted plates
        :param plate_image: Cropped license plate image
        :return: Perspective corrected plate image
        """
        if plate_image is None or plate_image.size == 0:
            return plate_image

        try:
            gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blur, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                return plate_image

            max_contour = max(contours, key=cv2.contourArea)
            epsilon = 0.02 * cv2.arcLength(max_contour, True)
            approx = cv2.approxPolyDP(max_contour, epsilon, True)
            if len(approx) != 4:
                return plate_image

            pts = approx.reshape(4, 2)
            rect = np.zeros((4, 2), dtype="float32")
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]
            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]


            (tl, tr, br, bl) = rect
            width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            max_width = max(int(width_a), int(width_b))

            height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
            max_height = max(int(height_a), int(height_b))


            dst = np.array([
                [0, 0],
                [max_width - 1, 0],
                [max_width - 1, max_height - 1],
                [0, max_height - 1]
            ], dtype="float32")
            
            M = cv2.getPerspectiveTransform(rect, dst)
            corrected = cv2.warpPerspective(plate_image, M, (max_width, max_height))

            return corrected

        except Exception as e:
            return plate_image

perspective_corrector = PerspectiveCorrector()