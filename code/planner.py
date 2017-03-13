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
            car
    ) -> Optional[str]:
        if car is None:
            return
        else:
            if car[1] > 5:
                return "left {:.0f}".format(car[1])
            else:
                return "forward {:.0f}".format(min(car[0] * 100, 50))
