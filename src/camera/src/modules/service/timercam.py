import datetime

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

        # define features:
        self.takePicture = TakePicture(self.config.getFeatureConfig('take_picture'))
        self.ftpsUpload = FTPSUpload(self.config.getFeatureConfig('ftps_upload'))

    def run(self, current_time) -> bool:
        if self.serviceIsActive():
            if self.serviceIsDueToRun(current_time):
                print('[TimerCam] Running ...')
                image_object = self.takePicture.takePicture()

                result = self.ftpsUpload.upload(image_object)

                if result['error']:
                    print('FTPSUplod failed! ' + result.response)
                    return
                
                print('[TimerCam] Done.')
                
                self.lastSuccessfulExecution = datetime.datetime.now()
            else:
                print('[TimerCam] Not due to run')
        else:
            print('[TimerCam] Inactive')

        return True

    def serviceIsDueToRun(self, current_time) -> bool:
        return self.lastSuccessfulExecution == None or self.lastSuccessfulExecution + datetime.timedelta(seconds=parseDuration(self.config.getValue('interval'))) <= current_time
            # return True
