import cv2
from analyzer import Analyzer
from planner import Planner

# author: Hendrik Werner s4549775

capture_path = "../capture.png"

image = cv2.imread(capture_path)
imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

analyzer = Analyzer(
    lower_ball=[[15, 128, 50]],
    upper_ball=[[25, 255, 255]],
    lower_blue=[[90, 128, 10]],
    upper_blue=[[120, 255, 255]],
    lower_red=[[170, 128, 50], [0, 128, 50]],
    upper_red=[[180, 255, 255], [10, 255, 255]],
)
planner = Planner(analyzer)
planner.plan(imageHSV)
