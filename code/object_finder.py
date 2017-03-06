# author: Hendrik Werner s4549775

import cv2
import numpy as np
import itertools
from typing import List
from helper_functions import angle, intersection


class ObjectFinder(object):
    def __init__(
            self,
            color_lower: List[List[int]],
            color_upper: List[List[int]],
            image_hsv: np.ndarray = None,
    ):
        """
        Initialize an object finder.

        :param image: The image in which to find objects in HSV format
        :param color_lower: The lower color thresholds (in HSV)
        :param color_upper: The upper color thresholds (in HSV)
        """
        assert len(color_lower) == len(color_upper)

        self.image = image_hsv
        self._color_lower = np.uint8(color_lower)
        self._color_upper = np.uint8(color_upper)

    def make_mask(
            self,
    ) -> np.ndarray:
        """
        Make a mask that captures pixels in a color range.

        :return: The generated mask
        """
        object_mask = np.zeros(self.image.shape[:2], dtype=np.uint8)
        for lower, upper in zip(self._color_lower, self._color_upper):
            object_mask += cv2.inRange(
                self.image,
                lower,
                upper,
            )

        object_mask = cv2.blur(object_mask, (3, 3))

        return object_mask

    def find_contours(
            self,
            mask: np.ndarray,
    ) -> List[np.ndarray]:
        """
        Find the contours in a mask.

        :param mask: The mask
        :return: The contours found
        """
        return cv2.findContours(
            mask,
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE,
        )[1]


class BallFinder(ObjectFinder):
    def find_round_object(
            self,
            contours,
    ) -> tuple:
        """
        Find a round object.

        :param contours: The contours found the in image.
        :return: ((x, y), radius) if an object is found
        """
        if len(contours):
            object = max(contours, key=cv2.contourArea)
            return cv2.minEnclosingCircle(object)

        return None, None

    def find_ball(
            self,
    ):
        """
        Find the ball.

        :return: ((x, y), radius) of the ball
        """
        mask = self.make_mask()
        contours = self.find_contours(mask)
        return self.find_round_object(contours)


class CarFinder(BallFinder):
    def smaller_angle(
            self,
            v1: np.ndarray,
            v2: np.ndarray,
            min_angle: int = 10,
    ) -> float:
        """
        Find the smaller angle between two vectors that is at least min_angle.

        :param v1: First vector
        :param v2: Second vector
        :param min_angle: Minimum angle (in deg) that is kept. Angles below
                          that will be discarded.
        :return: Minimum angle between v1 and v2 that is at least min_angle
        """
        min_angle = min_angle * np.pi / 180
        angles = [angle(v1, v2)]
        angles.append(np.pi - angles[0])
        filter(lambda a: a >= min_angle, angles)
        return min(angles)

    def find_angled_lines(
            self,
            contours,
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
        cv2.drawContours(contour_img, contours, -1, 255)
        contour_img = cv2.blur(contour_img, (2, 2))

        lines = cv2.HoughLinesP(contour_img, 1, np.pi / 180, 15, 5, 10)
        if lines is None:
            return []
        lines = lines.squeeze()

        vectors = [
            (i, [x2 - x1, y2 - y1]) for i, (x1, y1, x2, y2) in enumerate(lines)
            ]
        vector_combinations = itertools.combinations(vectors, 2)
        arrow_angle = arrow_angle * np.pi / 180
        best = min(
            vector_combinations,
            key=lambda c: abs(
                arrow_angle - self.smaller_angle(c[0][1], c[1][1])
            ),
        )
        best = [lines[i] for i, _ in best]

        return best

    def find_arrow(
            self,
            contours: list,
            arrow_angle: int = 32,
    ) -> tuple:
        """
        Find an arrow.

        :param contours: Contours of the arrow
        :param arrow_angle: Angle of the arrow
        :return: (None, None) if no arrow is found
                 ((center_x, center_y), (tip_x, tip_y)) otherwise
        """
        arr_pos = self.find_round_object(contours)[0]

        if not arr_pos:
            return None, None

        arr_lines = self.find_angled_lines(contours, arrow_angle)

        if len(arr_lines) < 2:
            return None, None

        arr_tip = intersection(*arr_lines)
        return arr_pos, arr_tip

    def find_car(
            self,
    ):
        """
        Find the car.

        :return: ((center_x, center_y), (tip_x, tip_y)) of the car
        """
        mask = self.make_mask()
        contours = self.find_contours(mask)
        return self.find_arrow(contours)
