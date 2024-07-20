import numpy as np
from chainner_ext import resize, ResizeFilter
from pepeline import fast_color_level


class Resize:

    def __init__(self, resize_dict: dict):
        size = resize_dict['size']
        interpolation = resize_dict.get('interpolation', 'linear')
        width = resize_dict.get('width')
        percent = resize_dict.get('percent', 1.0)
        spread = resize_dict.get('spread')
        spread_size = resize_dict.get('spread_size', 2800)
        color_fix = resize_dict.get('color_fix', False)
        gamma_correction = resize_dict.get('gamma_correction', False)

        self.gamma_correction = gamma_correction
        self.color_fix = color_fix
        self.size = size
        self.interpolation = interpolation
        self.width = width
        self.percent = percent / 100
        self.spread = spread
        self.spread_size = spread_size

    def run(self, img: np.ndarray) -> np.ndarray:
        interpolation_map = {
            'nearest': ResizeFilter.Nearest,
            'linear': ResizeFilter.Linear,
            'cubic_catrom': ResizeFilter.CubicCatrom,
            'cubic_mitchell': ResizeFilter.CubicMitchell,
            'cubic_bspline': ResizeFilter.CubicBSpline,
            'lanczos': ResizeFilter.Lanczos,
            'gauss': ResizeFilter.Gauss,
            'lagrange': ResizeFilter.Lagrange,
        }
        height, width = img.shape[:2]
        if self.width:
            height_k = height / width * self.size
            if width <= self.size:
                new_width = width * self.percent
                new_height = height * self.percent
            elif height < width and self.spread and self.spread_size < width:
                new_width = self.spread_size
                new_height = height / width * self.spread_size
            else:
                new_width = self.size
                new_height = height_k
        else:
            width_k = width / height * self.size
            if height <= self.size:
                new_width = width * self.percent
                new_height = height * self.percent
            else:
                new_width = width_k
                new_height = self.size
        img = resize(img.astype(np.float32), (int(new_width), int(new_height)), interpolation_map[self.interpolation],
                     gamma_correction=self.gamma_correction).squeeze()
        if self.color_fix:
            img = fast_color_level(img, in_high=250)
        return img
