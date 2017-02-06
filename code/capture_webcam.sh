#!/bin/bash

fswebcam -d "/dev/video$1" -l 1 --no-banner $2
