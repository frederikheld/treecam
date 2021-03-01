import datetime
import json

from modules.data.config import Config

from modules.feature.helloworld import HelloWorld
from modules.feature.takepicture import TakePicture
from modules.feature.postontwitter import PostOnTwitter
from modules.feature.ftpsupload import FTPSUpload

from modules.service.servicerunner import ServiceRunner
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

    # init ServiceRunner:
    serviceRunner = ServiceRunner(config.getServiceConfig('service_runner'))
    
    # init service TimerCam:
    timerCam = TimerCam(config.getServiceConfig('timer_cam'))
    serviceRunner.registerService(timerCam)

    # init service TwitterCam:
    twitterCam = TwitterCam(config.getServiceConfig('twitter_cam'))
    serviceRunner.registerService(twitterCam)

    # start ServiceRunner:
    serviceRunner.start()


main()
