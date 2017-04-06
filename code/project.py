import cv2
import yaml
from subprocess import run
from analyzer import Analyzer
from planner import Planner
from helper_functions import newest_frame

# author: Hendrik Werner s4549775

with open("config.yml") as conf_file:
    conf = yaml.safe_load(conf_file)

command = conf["executor"].split()
analyzer = Analyzer(
    conf["ball"],
    conf["blue_car"],
    conf["red_car"],
)
planner = Planner(
    analyzer,
    conf["car_length"],
)
webcam = cv2.VideoCapture(conf["capture_device"])

while cv2.waitKey(1) != 27:
    success, image = newest_frame(webcam)
    if success:
        cv2.imshow("Webcam", image)
        plan = planner.plan(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))
        if plan is not None:
            run(command + plan[1].split())  # red car
