# author: Hendrik Werner s4549775

import cv2
import sys
import numpy as np
from numpy.linalg import norm
from typing import List
from helper_functions import angle, as_deg
from object_finder import CarFinder, BallFinder


class Analyzer(object):
    def __init__(
            self,
            lower_ball: List[List[int]],
            upper_ball: List[List[int]],
            lower_blue: List[List[int]],
            upper_blue: List[List[int]],
            lower_red: List[List[int]],
            upper_red: List[List[int]],
    ):
        self._ball_finder = BallFinder(lower_ball, upper_ball)
        self._blue_car_finder = CarFinder(lower_blue, upper_blue)
        self._red_car_finder = CarFinder(lower_red, upper_red)

    def analyze_car(
            self,
            ball_pos: np.ndarray,
            car: np.ndarray,
            color: str = "",
    ) -> None:
        """
        Analyze a car.

        :param ball_pos: Position of the ball
        :param car: [[x, y], [tip_x, tip_y]] of the car
        :param color: Color of the car
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
            dist_to_ball = norm(car_ball_vector) / norm(car_vector) - 1

            print("{} Car:".format(color.capitalize()), car_pos, car_tip)
            print("Angle:", car_angle, "Distance:", dist_to_ball)

    def analyze(
            self,
            image_hsv: np.ndarray,
    ) -> None:
        image_hsv = cv2.medianBlur(image_hsv, 3)

        self._ball_finder.image = image_hsv
        self._blue_car_finder.image = image_hsv
        self._red_car_finder.image = image_hsv

        ball = self._ball_finder.find_ball()
        blue_car = self._blue_car_finder.find_car()
        red_car = self._red_car_finder.find_car()

        if ball is None:
            print("No ball found.", file=sys.stderr)
            return
        ball_pos, ball_radius = ball
        print("Ball:", ball_pos, ball_radius)

        self.analyze_car(ball_pos, blue_car, color="blue")
        self.analyze_car(ball_pos, red_car, color="red")
