#!/usr/bin/env python3

from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
sleep(2) # give camera time to get ready
camera.capture('output.jpg')

