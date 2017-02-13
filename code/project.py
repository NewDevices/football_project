import cv2
import numpy as np


# author: Hendrik Werner s4549775

capture_path = "../capture.png"

image = cv2.imread(capture_path)
imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
imageHSV = cv2.medianBlur(imageHSV, 5)

plt.imshow(cv2.cvtColor(imageHSV, cv2.COLOR_HSV2RGB))
plt.show()


def make_mask(
        hsv: np.ndarray
        , color_lower: list
        , color_upper: list
        , ed_iterations: int = 3
):
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
    object_mask = cv2.erode(object_mask, None, iterations=ed_iterations)
    object_mask = cv2.dilate(object_mask, None, iterations=ed_iterations)

    return object_mask


def find_contours(
        mask: np.ndarray
):
    """
    Find the contours in a mask.

    :param hsv: The mask
    :return: The contours found
    """
    return cv2.findContours(
        mask
        , cv2.RETR_LIST
        , cv2.CHAIN_APPROX_SIMPLE
    )


def find_round_object(
        contours
):
    """
    Find a round object.

    :param contours: The contours found the in image.
    :return: (x,y), radius if an object is found
    """
    if len(contours):
        object = max(contours, key=cv2.contourArea)
        return cv2.minEnclosingCircle(object)

    return None, None


ball_contours = find_contours(
    make_mask(imageHSV, [15, 150, 50], [25, 255, 255])
)[1]
ball_pos, ball_radius = find_round_object(ball_contours)
