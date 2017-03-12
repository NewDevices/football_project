import cv2
import yaml
from analyzer import Analyzer
from planner import Planner

# author: Hendrik Werner s4549775

with open("config.yml") as conf_file:
    conf = yaml.safe_load(conf_file)

capture_path = "../capture.png"

image = cv2.imread(capture_path)
imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

analyzer = Analyzer(
    conf["ball"]["lower"],
    conf["ball"]["upper"],
    conf["blue_car"]["lower"],
    conf["blue_car"]["upper"],
    conf["red_car"]["lower"],
    conf["red_car"]["upper"],
)
planner = Planner(analyzer)
planner.plan(imageHSV)
