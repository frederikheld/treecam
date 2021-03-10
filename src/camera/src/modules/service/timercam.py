"""
TreeCam service TimerCam
"""

import datetime
import logging

from modules.functions.stringparser import parseDuration

from modules.data.config import Config
from modules.data.image import Image

from modules.feature.takepicture import TakePicture
# from modules.feature.mocktakepicture import MockTakePicture as TakePicture
from modules.feature.ftpsupload import FTPSUpload

from modules.service.abstractservice import AbstractService

class TimerCam(AbstractService):

    def __init__(self, config):
        super().__init__(config)

        # get dependencies:
        self.logger = logging.getLogger(__name__)

        # define features:
        self.takePicture = TakePicture(self.config.getFeatureConfig('take_picture'))
        self.ftpsUpload = FTPSUpload(self.config.getFeatureConfig('ftps_upload'))

        # keep state:
        self.lastSuccessfulExecution = None

    def run(self, current_time) -> bool:
        """
        Returns False in case of error. Otherwise true.
        This means that 'inactive' counts as successful run that returns True!
        """
        if self.serviceIsActive():
            if self.serviceIsDueToRun(current_time):
                self.logger.info('Running ...')

                # provide image:

                if not self.config.getFeatureConfig('take_picture').getValue('active'):
                    self.logger.info('Feature take_picture is inactive. Service aborted.')
                    return False

                try:
                    image_object = self.takePicture.takePicture()
                except Exception as error:
                    self.logger.error('take_picture failed:' + str(error))

                # distribute image:

                if self.config.getFeatureConfig('ftps_upload').getValue('active', False):
                    try:
                        self.ftpsUpload.upload(image_object)
                    except Exception as error:
                        self.logger.error('ftps_upload failed: ' + str(error))
                        return False
                else:
                    self.logger.info('Feature ftps_upload is inactive.')

                # wrap-up:
                
                self.logger.info('Done.')
                self.lastSuccessfulExecution = datetime.datetime.now()
            else:
                self.logger.info('Not due to run')
        else:
            self.logger.info('Inactive')

        return True

    def serviceIsDueToRun(self, current_time) -> bool:
        return self.lastSuccessfulExecution == None or self.lastSuccessfulExecution + datetime.timedelta(seconds=parseDuration(self.config.getValue('interval'))) <= current_time
