import os
import datetime
import json
import logging

from modules.data.config import Config

from modules.service.servicerunner import ServiceRunner
from modules.service.timercam import TimerCam
from modules.service.twittercam import TwitterCam


def main():
    # testing stuff:
    # hello = HelloWorld()
    # hello.hello()
    # hello.hello('Fred')

    # load config:
    config = Config()
    config.loadConfigFromJSONFile(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json'))

    # configure logger:
    loggingConfig = config.getServiceConfig('global').getFeatureConfig('logging')
    logging.basicConfig(
        level=logging.getLevelName(loggingConfig.getValue('level')),
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        filename=loggingConfig.getValue('path')
    )

    # init ServiceRunner:
    serviceRunner = ServiceRunner(config.getServiceConfig('service_runner'))
    
    # init service TimerCam:
    timerCam = TimerCam(config.getServiceConfig('timer_cam'))
    serviceRunner.registerService(timerCam)

    # # init service TwitterCam:
    twitterCam = TwitterCam(config.getServiceConfig('twitter_cam'))
    serviceRunner.registerService(twitterCam)

    # start ServiceRunner:
    serviceRunner.start()


main()
