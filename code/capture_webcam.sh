#!/bin/bash

fswebcam -d "/dev/video$1" -r "160x120" --png 9 --no-banner $2
