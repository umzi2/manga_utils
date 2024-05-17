import numpy as np
from pepeline import screentone


class Halftone:
    def __init__(self, halftone_dict: dict):
        dot_size = halftone_dict.get("dot_size", 7)
        self.dot_size = dot_size
        pass

    def run(self, img: np.ndarray) -> np.ndarray:
        return screentone(np.squeeze(img), self.dot_size)
