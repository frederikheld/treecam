from datetime import datetime

from modules.data.config import Config
from modules.data.image import Image

from modules.feature.takepicture import TakePicture
from modules.feature.ftpsupload import FTPSUpload
from modules.service.abstractservice import AbstractService

class TimerCam(AbstractService):

    def __init__(self, config):
        super().__init__(config)

        # define features:
        self.takePicture = TakePicture(self.config.getFeatureConfig('take_picture'))
        self.ftpsUpload = FTPSUpload(self.config.getFeatureConfig('ftps_upload'))

    def run(self, current_time) -> Image:
        if self.serviceIsActive():
            if self.serviceIsDueToRun():
                image_object = self.takePicture.takePicture()

                result = self.ftpsUpload.upload(image_object)

                if result['error']:
                    print('FTPSUplod failed! ' + result.response)

        return True

    def serviceIsDueToRun(self) -> bool:
        return True # TODO: check if service is due to run
