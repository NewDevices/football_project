# author: Hendrik Werner s4549775

import cv2
import numpy as np
import itertools
from typing import List, Optional, Tuple
from helper_functions import as_rad, intersection, angle


class ObjectFinder(object):
    def __init__(
            self,
            thresholds: List[dict],
            image_hsv: np.ndarray = None,
    ):
        """
        Initialize an object finder.

        :param image: The image in which to find objects in HSV format
        :param thresholds: List of dicts containing "lower" and "upper" keys
                           which are lists of integers of the form [H, S, V]
        """
        self.image = image_hsv
        self._color_thresholds = thresholds
        for threshold in thresholds:
            threshold["lower"] = np.uint8(threshold["lower"])
            threshold["upper"] = np.uint8(threshold["upper"])

    def make_mask(
            self,
    ) -> None:
        """
        Make a mask that captures pixels in a color range.
        """
        self.mask = np.zeros(self.image.shape[:2], dtype=np.uint8)
        for threshold in self._color_thresholds:
            self.mask += cv2.inRange(
                self.image,
                threshold["lower"],
                threshold["upper"],
            )
        self.mask = cv2.blur(self.mask, (3, 3))

    def find_contours(
            self,
    ) -> None:
        """
        Find the contours in the mask.
        """
        self.contours = cv2.findContours(
            self.mask,
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE,
        )[1]

    def filter_contours(
            self,
            minimum_area: int=300,
    ) -> None:
        """
        Filter out unwanted contours.

        :param minimum_area: Contours with an area at least this size are kept
        """
        self.contours = [
            c for c in self.contours
            if cv2.contourArea(c) >= minimum_area
        ]


class BallFinder(ObjectFinder):
    def find_round_object(
            self,
    ) -> Optional[Tuple[np.ndarray, int]]:
        """
        Find a round object.

        :param contours: The contours found the in image.
        :return: ([x, y], radius) if an object is found
        """
        if len(self.contours):
            object = max(self.contours, key=cv2.contourArea)
            pos, radius = cv2.minEnclosingCircle(object)
            return np.rint(pos).astype(int), int(radius)

    def find_ball(
            self,
    ):
        """
        Find the ball.

        :return: ([x, y], radius) of the ball if it is found
        """
        self.make_mask()
        self.find_contours()
        self.filter_contours()
        return self.find_round_object()


class CarFinder(BallFinder):
    @staticmethod
    def angle_heuristic(
            desired_angle: float,
            v1: np.ndarray,
            v2: np.ndarray,
            min_angle: int = 10,
    ) -> float:
        """
        :param desired_angle: Desired angle in radians
        :param v1: First vector
        :param v2: Second vector
        :param min_angle: Minimum valid angle in degrees
        :return: Heuristic to minimize
        """
        min_angle = as_rad(min_angle)
        inner_angle = angle(v1, v2, True)
        if inner_angle < min_angle:
            return np.pi * 2
        return min(
            abs(desired_angle - inner_angle),
            abs(desired_angle - np.pi + inner_angle),
        )

    def find_angled_lines(
            self,
            arrow_angle: int,
    ) -> List[np.ndarray]:
        """
        Find two lines with a specific angle.

        :param contours: The contours to find the lines in
        :param arrow_angle: The angle in degrees
        :return: [l1, l2] where l1 and l2 are the lines which are closest to
                 the specified angle
        """
        approx_contours = [
            cv2.approxPolyDP(c, 10, closed=True).squeeze()
            for c in self.contours
        ]
        lines = []
        for contour in approx_contours:
            for p1, p2 in zip(contour, np.array([*contour[1:], contour[:1]])):
                lines.append(np.append(p1, p2))
        if len(lines) < 2:
            return lines

        vectors = [
            (i, [x2 - x1, y2 - y1]) for i, (x1, y1, x2, y2) in enumerate(lines)
            ]
        vector_combinations = itertools.combinations(vectors, 2)
        arrow_angle = as_rad(arrow_angle)
        best = min(
            vector_combinations,
            key=lambda c: self.angle_heuristic(arrow_angle, c[0][1], c[1][1])
        )
        best = [lines[i] for i, _ in best]

        return best

    def find_arrow(
            self,
            arrow_angle: int = 32,
    ) -> Optional[np.ndarray]:
        """
        Find an arrow.

        :param contours: Contours of the arrow
        :param arrow_angle: Angle of the arrow
        :return: [[center_x, center_y][tip_x, tip_y]] if an arrow is found
        """
        arrow = self.find_round_object()

        if arrow is None:
            return

        arr_pos = arrow[0]
        arr_lines = self.find_angled_lines(arrow_angle)

        if len(arr_lines) < 2:
            return

        arr_tip = intersection(*arr_lines)
        if arr_tip is None:
            return

        return np.rint([arr_pos, arr_tip]).astype(int)

    def find_ball(
            self,
    ):
        raise AttributeError("Use a BallFinder to find balls.")

    def find_car(
            self,
    ):
        """
        Find the car.

        :return: [[center_x, center_y][tip_x, tip_y]] of the car if it is found
        """
        self.make_mask()
        self.find_contours()
        self.filter_contours()
        return self.find_arrow()
