import cv2
import numpy as np
import itertools
from typing import Optional

# author: Hendrik Werner s4549775

capture_path = "../capture.png"

image = cv2.imread(capture_path)
imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
imageHSV = cv2.medianBlur(imageHSV, 3)


def make_mask(
        hsv: np.ndarray
        , color_lower: list
        , color_upper: list
) -> np.ndarray:
    """
    Make a mask that captures pixels in a color range.

    :param hsv: The image in HSV format
    :param color_lower: The lower color threshold (in HSV)
    :param color_upper: The upper color threshold (in HSV)
    :param ed_iterations: The number of iterations for erosion and dilation
    :return: The generated mask
    """
    color_lower = np.uint8(color_lower)
    color_upper = np.uint8(color_upper)

    object_mask = cv2.inRange(hsv, color_lower, color_upper)
    object_mask = cv2.blur(object_mask, (3, 3))

    return object_mask


def find_contours(
        mask: np.ndarray
) -> tuple:
    """
    Find the contours in a mask.

    :param mask: The mask
    :return: The contours found
    """
    return cv2.findContours(
        mask
        , cv2.RETR_LIST
        , cv2.CHAIN_APPROX_SIMPLE
    )


def find_round_object(
        contours
) -> tuple:
    """
    Find a round object.

    :param contours: The contours found the in image.
    :return: (x,y), radius if an object is found
    """
    if len(contours):
        object = max(contours, key=cv2.contourArea)
        return cv2.minEnclosingCircle(object)

    return None, None


def normalize(
        vector: np.ndarray
) -> np.ndarray:
    """
    :param vector: A vector
    :return: The normalized vector
    """
    return vector / np.linalg.norm(vector)


def angle(
        v1: np.ndarray, v2: np.ndarray
) -> np.float64:
    """
    :param v1: One vector
    :param v2: Another vector
    :return: Angle between the two vectors
    """
    v1 = normalize(v1)
    v2 = normalize(v2)
    return np.arccos(np.clip(np.dot(v1, v2), a_min=-1, a_max=1))


def find_angled_lines(
        contours
        , arrow_angle: int
) -> list:
    """
    Find two lines with a specific angle.

    :param contours: The contours to find the lines in
    :param arrow_angle: The angle in degrees
    :return: (l1, l2) where l1 and l2 are the lines which are closest to the
             specified angle
    """
    contour_img = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.drawContours(contour_img, contours, -1, 255)
    contour_img = cv2.blur(contour_img, (2, 2))

    lines = cv2.HoughLinesP(contour_img, 1, np.pi / 180, 15, 5, 10).squeeze()

    vectors = [
        (i, [x2 - x1, y2 - y1]) for i, (x1, y1, x2, y2) in enumerate(lines)
        ]
    vector_combinations = itertools.combinations(vectors, 2)
    arrow_angle = arrow_angle * np.pi / 180
    best = min(
        vector_combinations
        , key=lambda c: abs(arrow_angle - angle(c[0][1], c[1][1]))
    )
    best = [lines[i] for i, _ in best]

    return best


def find_intersection(
        l1: np.ndarray
        , l2: np.ndarray
) -> Optional[np.ndarray]:
    """
    Find the intersection of two lines if it exists. Lines are specified as
    pairs of points: [[x1, y1], [x2, y2]].

    This function was inspired by http://stackoverflow.com/a/7448287/4637060.

    :param l1: The first line
    :param l2: The second line
    :return: The intersection if it exists
    """
    l1 = l1.reshape((2, 2))
    l2 = l2.reshape((2, 2))

    x = l2[0] - l1[0]
    d1 = l1[1] - l1[0]
    d2 = l2[1] - l2[0]
    cross = np.cross(d1, d2)

    if abs(cross) < 1e-8:
        return

    t1 = (x[0] * d2[1] - x[1] * d2[0]) / cross
    return l1[0] + d1 * t1


def find_car(
        contours: list
        , arrow_angle: int = 32
):
    """
    Find a car.

    :param contours: Contours of the car
    :param arrow_angle: Angle of the car arrow
    :return: None, None if no car is found
             car_center, car_tip otherwise
    """
    car_pos, _ = find_round_object(contours)

    if not car_pos:
        return None, None

    car_lines = find_angled_lines(contours, arrow_angle)

    if len(car_lines) < 2:
        return None, None

    car_tip = find_intersection(*car_lines)
    return car_pos, car_tip


ball_contours = find_contours(
    make_mask(imageHSV, [15, 150, 50], [25, 255, 255])
)[1]
ball_pos, ball_radius = find_round_object(ball_contours)

blue_car_contours = find_contours(
    make_mask(imageHSV, [90, 128, 10], [120, 255, 255])
)[1]
blue_car_pos, blue_car_tip = find_car(blue_car_contours)
