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
	* Unix: You need to compile OpenCV yourself, because we use modules that are not supported in the python package.

### Java

## Confuguration
A YAML config file is provided to ease configuration `code/config.yml`

* `capture_device`: ID of the capture device to use. Probably 0 if you only have one camera connected.
* `car_length`: Length of the car in millimeters. Note that this is measured from the center of the arrow to the tip.
* `ball`: [Color thresholds](#color-thresholds) for the ball.
* `blue_car`: [Color thresholds](#color-thresholds) for the blue car.
* `red_car`: [Color thresholds](#color-thresholds) for the blue car.

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
