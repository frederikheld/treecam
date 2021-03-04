"""
Mocked version of the TreeCam feature TakePicture
which loads a picture from a file on disk.
"""

import os
import io

from modules.data.image import Image


class MockTakePicture:

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

        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'pictures', 'dummy.png')

        with io.open(file_path, 'rb') as file_handler:
            image_object = Image()
            image_object.storeImage(
                io.BytesIO(file_handler.read()),
                'png'
            )

        return image_object
