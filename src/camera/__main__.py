import datetime
import json

from modules.data.config import Config

from modules.feature.helloworld import HelloWorld
from modules.feature.takepicture import TakePicture
from modules.feature.postontwitter import PostOnTwitter
from modules.feature.ftpsupload import FTPSUpload

from modules.service.timercam import TimerCam
from modules.service.twittercam import TwitterCam


def main():
    # testing stuff:
    hello = HelloWorld()
    hello.hello()
    hello.hello('Fred')

    # load config:
    config = Config()
    config.loadConfigFromJSONFile('config.json')

    # service TimerCam:
    timerCam = TimerCam(config.getServiceConfig('timer_cam'))
    timerCam.run(datetime.datetime.now())

    # service TwitterCam:
    twitterCam = TwitterCam(config.getServiceConfig('twitter_cam'))
    twitterCam.run(datetime.datetime.now())

    # # take picture:
    # takePicture = TakePicture(config.getModuleConfig('take_picture'))
    # image_object = takePicture.takePicture()

    # # post picture to Twitter:
    # if config.getModuleConfig('post_on_twitter').getValue('active'):
    #     postOnTwitter = PostOnTwitter(config.getModuleConfig('post_on_twitter'))
    #     result = postOnTwitter.post(
    #         'Hello Twitter! ' + image_object.get_timestamp_created().strftime(config.getGlobalConfigValue('filename_time_format')),
    #         image_object,
    #         in_reply_to_status_id = None
    #     )

    #     if result['error']:
    #         print('PostOnTwitter failed! ' + result.respones)

    # # upload to FTPS server:
    # if config.getModuleConfig('ftps_upload').getValue('active'):
    #     ftpsUpload = FTPSUpload(config.getModuleConfig('ftps_upload'))
    #     result = ftpsUpload.upload(image_object)

    #     if result['error']:
    #         print('FTPSUplod failed! ' + result.response)


main()
