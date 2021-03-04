"""
TreeCam feature TakePicture
"""

import io
import time
import picamera

from modules.data.image import Image


class TakePicture:

    def __init__(self, config_object):
        """
        Parameters:
            config_object | Config object | Module-specific configuration
        """
        self.config = config_object

    # mocked function for testing on non-RasPi devices:
    def takePicture(self):
        """
            Takes a picture with the RasPi cam and returns
            it as a BytesIO object.

            Parameter:
                None

            Return:
                Image object
        """
       
        bytes_stream = io.BytesIO()
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.start_preview()
            time.sleep(2) # Give camera some time to get ready
            camera.capture(bytes_stream, 'png')

        image_object = Image()
        image_object.storeImage(
            bytes_stream,
            'png'
        )

        return image_object
