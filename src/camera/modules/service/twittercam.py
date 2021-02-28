from datetime import datetime

from modules.data.config import Config
from modules.data.image import Image

from modules.service.abstractservice import AbstractService
from modules.feature.takepicture import TakePicture
from modules.feature.postontwitter import PostOnTwitter

class TwitterCam(AbstractService):

    def __init__(self, config):
        super().__init__(config)

        # define features:
        self.takePicture = TakePicture(self.config.getFeatureConfig('take_picture'))
        self.postOnTwitter = PostOnTwitter(self.config.getFeatureConfig('post_on_twitter'))

    def run(self, current_time) -> bool:
        if self.serviceIsActive():
            if self.serviceIsDueToRun():
                image_object = self.takePicture.takePicture()

                result = self.postOnTwitter.post(
                    'Hello Twitter! ' + image_object.getTimestampCreated().strftime(self.config.getFeatureConfig('take_picture').getValue('filename_time_format')),
                    image_object,
                    in_reply_to_status_id = None
                )

                if result['error']:
                    print('FTPSUplod failed! ' + result.response)

        return True

    def serviceIsDueToRun(self) -> bool:
        return True # TODO: check if service is due to run
