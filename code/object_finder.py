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
        return self.find_round_object()


class CarFinder(BallFinder):
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
        contour_img = np.zeros(self.image.shape[:2], dtype=np.uint8)
        cv2.drawContours(contour_img, self.contours, -1, 255)
        contour_img = cv2.blur(contour_img, (2, 2))

        lines = cv2.HoughLinesP(contour_img, 1, np.pi / 180, 30, 10, 20)
        if lines is None:
            return []
        lines = lines.squeeze()
        if len(lines.shape) == 1:
            return [lines]

        vectors = [
            (i, [x2 - x1, y2 - y1]) for i, (x1, y1, x2, y2) in enumerate(lines)
            ]
        vector_combinations = itertools.combinations(vectors, 2)
        arrow_angle = as_rad(arrow_angle)
        best = min(
            vector_combinations,
            key=lambda c: abs(
                arrow_angle - angle(c[0][1], c[1][1])
            ),
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
        return self.find_arrow()
