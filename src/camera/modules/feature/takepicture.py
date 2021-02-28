"""
TreeCam feature TakePicture
"""

import io

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
                ByteIO image object
        """

        file_path = 'pictures/dummy.png'

        with io.open(file_path, 'rb') as file_handler:
            image_object = Image()
            image_object.storeImage(
                io.BytesIO(file_handler.read()),
                'png'
            )

        return image_object
