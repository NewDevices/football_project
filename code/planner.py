# author: Hendrik Werner s4549775

import numpy as np
from analyzer import Analyzer


class Planner(object):
    def __init__(
            self,
            analyzer: Analyzer,
    ):
        self.analyzer = analyzer

    def plan(
            self,
            image_hsv: np.ndarray,
    ):
        info = self.analyzer.analyze(image_hsv)
        if info is None:
            return
        blue_car, red_car = info
