#!/usr/bin/env python3

from time import sleep
from picamera import PiCamera

print("Hello Python!")

try:
    camera = PiCamera()
except:
    print("could not init camera object")
    raise

try:
    camera.resolution = (1024, 768)
except:
    print("could not set resolution")
    raise

try:
    camera.start_preview()
except:
    print("could not start preview")
    raise

sleep(2) # give camera time to get ready

try:
    camera.capture('output.jpg')
except:
    print("could not capture picture")
    raise

exit()
