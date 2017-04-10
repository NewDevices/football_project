# SoccerBot

Autonomous football playing robot(s).

## Dependencies
### Python
Tested with Python 3.5 and 3.6.

* pyyaml (>= 3.12)
* opencv (>= 3.2)

### Java
* JDK (>= 6)
* LeJOS (== 9.1)

## Installation
### Python
1. [Install Python](https://www.python.org/downloads/) and pip
1. Install PyYAML

	`pip install pyyaml`
1. Install OpenCV

	* Windows: `pip install opencv-python`
	* Unix: You need to [compile OpenCV yourself](http://opencv.org/releases.html), because we use modules that are not supported in the python package.

### Java

## Confuguration
A YAML config file is provided to ease configuration `code/config.yml`

* `capture_device`: ID of the capture device to use. Probably 0 if you only have one camera connected.
* `car_length`: Length of the car in millimeters. Note that this is measured from the center of the arrow to the tip.
* `ball`: [Color thresholds](#color-thresholds) for the ball.
* `blue_car`: [Color thresholds](#color-thresholds) for the blue car.
* `red_car`: [Color thresholds](#color-thresholds) for the red car.

### Color thresholds
Color thresholds are provided as lists of lower/upper HSV pairs, for example:

	ball:
	  - lower: [0, 0, 0]
	    upper: [180, 255, 255]

This captures all pixels in the image.

## Usage
	# Go to the code directory
	cd code/
	# Run the project
	python project.py
	
## Robots
Theoretically you can use any robot you want. The system has a modular architecture that allows you to exchange parts of the system. If you decide to use another robot you must provide a system to connect to it yourself.

The robot we used was a [3-Motor Chassis](http://nxtprograms.com/NXT2/3-motor_chassis/steps.html) for the Lego NXT.

![Lego NXT 3-Motor Chassis](http://nxtprograms.com/NXT2/3-motor_chassis/DCP_9774.JPG)

### Executor
An executor is needed to execute the plan of action generated by the planner. We provide an executor for the Lego robot we used, but you can easily make your own if you want to use another method of communication, another robot etc.

#### Interface
The executor needs to provide the following interface:

	forward <integer> # Move forward by <integer> millimeters
	backward <integer> # Move backward by <integer> millimeters
	left <integer> # Turn left by <integer> degrees
	right <integer> # Turn right by <integer> degrees
	down # Move the ball catcher down
	up # Move the ball catcher up
	
You can take this as input via stdin, as parameters, or anything else. Just take care to call it correctly in the Python code.