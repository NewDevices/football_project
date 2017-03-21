# author: Hendrik Werner s4549775

import cv2
import numpy as np
from typing import Optional, Tuple


def normalize(
        vector: np.ndarray,
) -> np.ndarray:
    """
    :param vector: A vector
    :return: The normalized vector
    """
    return vector / np.linalg.norm(vector)


def angle(
        v1: np.ndarray,
        v2: np.ndarray,
        inner: bool=False,
) -> float:
    """
    :param v1: One vector
    :param v2: Another vector
    :param inner: Whether to calculate the inner angle
    :return: Angle between the two vectors
    """
    v1 = normalize(v1)
    v2 = normalize(v2)
    angle = np.arccos(np.clip(np.dot(v1, v2), a_min=-1, a_max=1))
    if inner:
        return angle
    cross = np.cross(v1, v2)
    return angle if cross <= 0 else np.pi * 2 - angle


def as_deg(
        angle_rad: float,
) -> float:
    """
    :param angle_rad: An angle in radians
    :return: The angle in degrees
    """
    return angle_rad * 180 / np.pi


def as_rad(
        angle_deg: float,
) -> float:
    """
    :param angle_deg: An angle in degrees
    :return: The angle in radians
    """
    return angle_deg * np.pi / 180


def intersection(
        l1: np.ndarray,
        l2: np.ndarray,
) -> Optional[np.ndarray]:
    """
    Find the intersection of two lines if it exists. Lines are specified as
    pairs of points: [[x1, y1], [x2, y2]].

    This function was inspired by
    http://stackoverflow.com/a/7448287/4637060.

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


def newest_frame(
        capture_device: int=0
) -> Tuple[bool, Optional[np.ndarray]]:
    """
    Capture the newest frame from the webcam.

    This should not be hard but the cv2.CAP_PROP_BUFFERSIZE property cannot be
    set or retrieved from the camera. We do not know why this is exactly. There
    are several proposed workarounds for this problem and this is one of them.

    The capture device is opened, a frame is captured and then it is closed
    again. This circumvents the internal frame buffer and allows us to capture
    the newest frame.

    :param capture_device: Capture device (ID / filename)
    :return: (success, frame)
    """
    webcam = cv2.VideoCapture(capture_device)
    capture = webcam.read()
    webcam.release()
    return capture
