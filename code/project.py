import cv2
import numpy as np


# author: Hendrik Werner s4549775


def find_round_object(
        hsv: np.ndarray
        , color_lower: list
        , color_upper: list
        , ed_iterations: int = 3
):
    """
    Find a round object.

    :param hsv: The image in HSV format
    :param color_lower: The lower color threshold (in HSV)
    :param color_upper: The upper color threshold (in HSV)
    :param ed_iterations: The number of iterations for erosion and dilation
    :return: (x,y), radius if an object is found
    """
    color_lower = np.uint8(color_lower)
    color_upper = np.uint8(color_upper)

    object_mask = cv2.inRange(hsv, color_lower, color_upper)
    object_mask = cv2.erode(object_mask, None, iterations=ed_iterations)
    object_mask = cv2.dilate(object_mask, None, iterations=ed_iterations)

    object_contours = cv2.findContours(
        object_mask
        , cv2.RETR_LIST
        , cv2.CHAIN_APPROX_SIMPLE
    )[1]

    if len(object_contours):
        object = max(object_contours, key=cv2.contourArea)

        return cv2.minEnclosingCircle(object)
