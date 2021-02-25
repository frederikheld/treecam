from time import sleep
from picamera import PiCamera

print("Hello again!")

try:
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(2) # Camera warm-up time
    camera.capture('foo.jpg')
except:
    print("Error: ", sys.exc_info()[0])
    raise
    