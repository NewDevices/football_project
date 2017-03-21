# author: Hendrik Werner s4549775

import cv2
import sys
import numpy as np
from numpy.linalg import norm
from typing import List, Optional, Tuple
from helper_functions import angle, as_deg
from object_finder import CarFinder, BallFinder


class Analyzer(object):
    @staticmethod
    def show_positions(
            image_hsv: np.ndarray,
            ball: Optional[Tuple[np.ndarray, int]]=None,
            blue_car: Optional[Tuple[np.ndarray, np.ndarray]]=None,
            red_car: Optional[Tuple[np.ndarray, np.ndarray]]=None,
    ) -> None:
        """
        Show the positions of the objects that were found.

        :param image_hsv: Image in HSV format
        :param ball: (ball_position, ball_radius)
        :param blue_car: (blue_car_pos, blue_car_tip)
        :param red_car: (red_car_pos, red_car_tip)
        """
        image = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
        if ball is not None:
            cv2.circle(image, tuple(ball[0]), ball[1], (255, 0, 0), 2)
        if blue_car is not None:
            cv2.arrowedLine(
                image,
                tuple(blue_car[0]),
                tuple(blue_car[1]),
                (0, 0, 255), 2,
            )
        if red_car is not None:
            cv2.arrowedLine(
                image,
                tuple(red_car[0]),
                tuple(red_car[1]),
                (0, 255, 0), 2,
            )
        cv2.imshow("Positions", image)

    def __init__(
            self,
            ball_thresholds: List[dict],
            blue_thresholds: List[dict],
            red_thresholds: List[dict],
    ):
        self._ball_finder = BallFinder(ball_thresholds)
        self._blue_car_finder = CarFinder(blue_thresholds)
        self._red_car_finder = CarFinder(red_thresholds)

    def analyze_car(
            self,
            ball_pos: np.ndarray,
            car: np.ndarray,
            color: str = "",
    ) -> Optional[Tuple[float, float]]:
        """
        Analyze a car.

        :param ball_pos: Position of the ball
        :param car: [[x, y], [tip_x, tip_y]] of the car
        :param color: Color of the car
        :return: (dist_to_ball, car_angle) if the car is not None
        """
        if car is None:
            print("No {} car found.".format(color), file=sys.stderr)
        else:
            car_pos, car_tip = car
            car_vector = car_tip - car_pos
            car_ball_vector = ball_pos - car_pos
            car_angle = as_deg(angle(
                car_vector,
                car_ball_vector,
            ))
            dist_to_ball = float(norm(car_ball_vector) / norm(car_vector) - 1)

            return dist_to_ball, car_angle

    def analyze(
            self,
            image_hsv: np.ndarray,
    ) -> Optional[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """
        Analyze an image and look for a ball and the blue and red car. If a
        ball is found return the cars's relations to the ball.

        :param image_hsv: Image in HSV format
        :return: blue_car_info, red_car_info
        """
        image_hsv = cv2.medianBlur(image_hsv, 3)

        self._ball_finder.image = image_hsv
        self._blue_car_finder.image = image_hsv
        self._red_car_finder.image = image_hsv

        ball = self._ball_finder.find_ball()
        blue_car = self._blue_car_finder.find_car()
        red_car = self._red_car_finder.find_car()

        cv2.imshow("Blue Mask", self._blue_car_finder.mask)
        cv2.imshow("Red Mask", self._red_car_finder.mask)

        if ball is None:
            print("No ball found.", file=sys.stderr)
            return
        ball_pos, ball_radius = ball

        self.show_positions(image_hsv, ball, blue_car, red_car)

        blue_car_info = self.analyze_car(
            ball_pos,
            blue_car,
            color="blue"
        )
        red_car_info = self.analyze_car(
            ball_pos,
            red_car,
            color="red"
        )
        return blue_car_info, red_car_info
