import cv2
import numpy as np
from pepeline import fast_color_level


class Sharp:
    def __init__(self, sharp_dict: dict):
        diapason_white = sharp_dict.get("diapason_white", -1)
        diapason_black = sharp_dict.get("diapason_black", -1)
        high_input = sharp_dict.get("high_input", 255)
        low_input = sharp_dict.get("low_input", 0)
        gamma = sharp_dict.get("gamma", 1.0)
        cenny = sharp_dict.get("cenny", False)
        self.diapason_white = diapason_white
        self.high_input = high_input
        self.low_input = low_input
        self.gamma = 1 / gamma
        self.cenny = cenny
        self.diapason_black = diapason_black / 255

    def __cenny(self, image_float: np.ndarray) -> np.ndarray:
        image = (image_float * 255).astype(np.uint8)
        edges = np.clip(cv2.Canny(image, 750, 800, apertureSize=3, L2gradient=False) * -1 + 255, 0, 1)
        return np.where(edges, image_float, 0)

    def __diapason_white(self, image_float: np.ndarray) -> np.ndarray:
        image = (image_float * 255).astype(np.uint8)
        median_image = cv2.medianBlur(image, 3)
        mask = median_image <= 255 - self.diapason_white
        return np.where(mask, image_float, 1.0)

    def __diapason_black(self, image: np.ndarray) -> np.ndarray:
        _, black_mask = cv2.threshold(image, self.diapason_black, 1, cv2.THRESH_BINARY)
        blur = cv2.GaussianBlur(black_mask, (3, 3), 0)
        _, img = cv2.threshold(blur, 0.6, 1.0, cv2.THRESH_BINARY_INV)

        return image - img

    def __color_levels(self, image: np.ndarray) -> np.ndarray:
        return fast_color_level(image, self.low_input, self.high_input, 0, 255, self.gamma)

    def run(self, image: np.ndarray) -> np.ndarray:

        if self.low_input != 0 or self.high_input != 1 or self.gamma != 1:
            image = self.__color_levels(image)
        if self.cenny:
            image = self.__cenny(image)
        if self.diapason_white >= 0:
            image = self.__diapason_white(image)
        if self.diapason_black >= 0:
            image = self.__diapason_black(image)
        return image
