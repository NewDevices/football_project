import cv2
import yaml
from analyzer import Analyzer
from planner import Planner

# author: Hendrik Werner s4549775

with open("config.yml") as conf_file:
    conf = yaml.safe_load(conf_file)

analyzer = Analyzer(
    conf["ball"],
    conf["blue_car"],
    conf["red_car"],
)
planner = Planner(analyzer)
webcam = cv2.VideoCapture(conf["capture_device"])

key = None
while key != 27:
    success, image = webcam.read()
    if success:
        imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        cv2.imshow("Webcam", image)
        key = cv2.waitKey(100)
        planner.plan(imageHSV)
