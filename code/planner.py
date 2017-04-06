# author: Hendrik Werner s4549775

import numpy as np
from analyzer import Analyzer
from typing import Optional, Tuple


class Planner(object):
    def __init__(
            self,
            analyzer: Analyzer,
            car_length: int,
    ):
        self.analyzer = analyzer
        self.car_length = car_length

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
            if car[0] < 0:
                action = ("backward", min(-car[0], .5) * self.car_length)
            elif 5 < car[1] <= 180:
                action = ("left", car[1])
            elif 180 < car[1] < 355:
                action = ("right", 360 - car[1])
            elif car[0] > .1 * self.car_length:
                action = ("forward", min(car[0], .5) * self.car_length)
            else:
                return "down"
            return "{:s} {:.0f}".format(*action)
