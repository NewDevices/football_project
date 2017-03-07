# author: Hendrik Werner s4549775

import cv2
import sys
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

    def analyze(
            self,
            image_hsv,
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

        if blue_car is None:
            print("No blue car found.", file=sys.stderr)
        else:
            blue_car_pos, blue_car_tip = blue_car
            blue_car_vector = blue_car_tip - blue_car_pos
            blue_car_ball_vector = ball_pos - blue_car_pos
            blue_car_angle = as_deg(angle(
                blue_car_vector,
                blue_car_ball_vector,
            ))

            print("Blue Car:", blue_car_pos, blue_car_tip)
            print("Angle:", blue_car_angle)

        if red_car is None:
            print("No red car found.", file=sys.stderr)
        else:
            red_car_pos, red_car_tip = red_car
            red_car_vector = red_car_tip - red_car_pos
            red_car_ball_vector = ball_pos - red_car_pos
            red_car_angle = as_deg(angle(
                red_car_vector,
                red_car_ball_vector,
            ))

            print("Red Car:", red_car_pos, red_car_tip)
            print("Angle:", red_car_angle)
