import datetime
import logging

from modules.functions.stringparser import parseDuration

from modules.data.config import Config
from modules.data.image import Image

from modules.feature.takepicture import TakePicture
# from modules.feature.mocktakepicture import MockTakePicture
from modules.feature.ftpsupload import FTPSUpload

from modules.service.abstractservice import AbstractService

class TimerCam(AbstractService):

    def __init__(self, config):
        super().__init__(config)

        self.lastSuccessfulExecution = None

        self.logger = logging.getLogger(__name__)

        # define features:
        self.takePicture = TakePicture(self.config.getFeatureConfig('take_picture'))
        self.ftpsUpload = FTPSUpload(self.config.getFeatureConfig('ftps_upload'))

    def run(self, current_time) -> bool:
        if self.serviceIsActive():
            if self.serviceIsDueToRun(current_time):
                self.logger.info('Running ...')
                image_object = self.takePicture.takePicture()

                result = self.ftpsUpload.upload(image_object)

                if result['error']:
                    self.logger.error('FTPSUplod failed! ' + result.response)
                    return
                # TODO: switch from result['error'] approch to raising and catching exceptions (see ftpsupload)
                
                self.logger.info('Done.')
                
                self.lastSuccessfulExecution = datetime.datetime.now()
            else:
                self.logger.info('Not due to run')
        else:
            self.logger.info('Inactive')

        return True

    def serviceIsDueToRun(self, current_time) -> bool:
        return self.lastSuccessfulExecution == None or self.lastSuccessfulExecution + datetime.timedelta(seconds=parseDuration(self.config.getValue('interval'))) <= current_time
