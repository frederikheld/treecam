import datetime
import logging
import sys

from modules.data.config import Config
from modules.data.image import Image

from modules.functions.datetimeparser import *

from modules.feature.takepicture import TakePicture
from modules.feature.postontwitter import PostOnTwitter

from modules.service.abstractservice import AbstractService

class TwitterCam(AbstractService):

    def __init__(self, config_object):
        super().__init__(config_object)

        # get dependencies:
        self.logger = logging.getLogger(__name__)

        # define features:
        self.takePicture = TakePicture(self.config.getFeatureConfig('take_picture'))
        self.postOnTwitter = PostOnTwitter(self.config.getFeatureConfig('post_on_twitter'))

        # keep state:
        self.shots = []
        for shot in self.config.getValue('shots'):
            shot['last_execution_time'] = None
            self.shots.append(shot)
        self.shotToExecuteNext = None

    def getShotToExecuteNext():
        return self.shotToExecuteNext

    def run(self, current_time) -> bool:
        if self.serviceIsActive():
            
            shot_to_be_run = self.getShotToBeExecuted(current_time)

            if shot_to_be_run == None:
                self.logger.info('Not due to run')

            else:
                self.logger.info('Running ...')
                image_object = self.takePicture.takePicture()

                try:
                    result = self.postOnTwitter.post(
                        self.shots[shot_to_be_run]['message'],
                        image_object,
                        in_reply_to_status_id = None
                    )
                    self.shots[shot_to_be_run]['last_execution_time'] = datetime.datetime.now()

                except ConnectionError as error:
                    self.logger.warning(error)

                self.logger.info('Done.')

        else:
            self.logger.info('Inactive')

        return True

    def getShotToBeExecuted(self, current_time) -> int:
        # HOW THIS ALGORITHM WORKS:
        #
        # Goal:
        #
        # get the latest shot in the list that
        #   > is not past now()
        #   > was not already run today
        #
        # Algorithm:
        #
        # start with first shot:
        #   > was it aleady run today?
        #       > yes: skip it
        #       > no: is it <= now()?
        #           > yes: is the next shot also <= now()?
        #               > yes: skip and repeat with next --> all over-due shots will be skipped!
        #               > no: return True
        #           > no: return False --> no shots to run now
        
        def shotAlreadyExecutedToday(shot_id):
            last_execution_time = self.shots[shot_id]['last_execution_time']

            if last_execution_time == None:
                return False

            midnight = datetime.datetime(
                year=last_execution_time.year,
                month=last_execution_time.month,
                day=last_execution_time.day)
           
            return last_execution_time > midnight

        now = getTimeOfDayFromString(datetime.datetime.now().strftime(TIME_STRING_FORMAT))

        for i in range(len(self.shots)):
            self.logger.info('Shot scheduled for ' + self.shots[i]['time_of_day'] + ':')
            if self.shots[i]['last_execution_time']:
                last_time_executed = self.shots[i]['last_execution_time'].strftime(DATETIME_STRING_FORMAT)
            else:
                last_time_executed = 'never'
            self.logger.info('ℹ last time executed: ' + last_time_executed)

            if getTimeOfDayFromString(self.shots[i]['time_of_day']) <= now:
                self.logger.info('✔️ not in future')

                if len(self.shots) > i+1 and getTimeOfDayFromString(self.shots[i+1]['time_of_day']) <= now:
                    self.logger.info('x next shot not in future --> pass')
                
                    if not shotAlreadyExecutedToday(i):
                        self.logger.warn('⚠️ ' + 'Shot scheduled for ' + self.shots[i]['time_of_day'] + ' is over-due and will be skipped!')

                else:
                    self.logger.info('✔️ next shot in future')
                    if not shotAlreadyExecutedToday(i):
                        self.logger.info('✔️ not exectued today --> execute')
                        return i
                    else:
                        self.logger.info('⚠️ already executed today --> no shot to run')
                        return None

            else:
                self.logger.info('x in future --> pass')
                pass