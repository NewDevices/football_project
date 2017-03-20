# author: Hendrik Werner s4549775

import numpy as np
from analyzer import Analyzer
from typing import Optional, Tuple


class Planner(object):
    def __init__(
            self,
            analyzer: Analyzer,
    ):
        self.analyzer = analyzer

    def plan(
            self,
            image_hsv: np.ndarray,
    ) -> Optional[Tuple[Optional[str], Optional[str]]]:
        info = self.analyzer.analyze(image_hsv)
        if info is None:
            return
        return self._plan_car(info[0]), self._plan_car(info[1])

    def _plan_car(
            self,
            car: Optional[Tuple[float, float]],
    ) -> Optional[str]:
        if car is None:
            return
        else:
            if 5 < car[1] <= 180:
                direction = ("left", car[1])
            elif 180 < car[1] < 355:
                direction = ("right", 360 - car[1])
            else:
                return "forward {:.0f}".format(min(car[0] * 100, 50))
            return "{} {:.0f}".format(*direction)
