import datetime

from modules.data.config import Config
from modules.data.image import Image

from modules.functions.datetimeparser import *

from modules.feature.takepicture import TakePicture
from modules.feature.postontwitter import PostOnTwitter

from modules.service.abstractservice import AbstractService

class TwitterCam(AbstractService):

    def __init__(self, config_object):
        super().__init__(config_object)

        # define features:
        self.takePicture = TakePicture(self.config.getFeatureConfig('take_picture'))
        self.postOnTwitter = PostOnTwitter(self.config.getFeatureConfig('post_on_twitter'))

        # keep state:
        self.shots = []
        for shot in self.config.getValue('shots'):
            shot['last_execution_time'] = None
            self.shots.append(shot)
        self.shotToExecuteNext = None

        print(self.shots)

    def getShotToExecuteNext():
        return self.shotToExecuteNext

    def run(self, current_time) -> bool:
        if self.serviceIsActive():
            
            shot_to_be_run = self.getShotToBeExecuted(current_time)

            if shot_to_be_run == None:
                print('[TwitterCam] Not due to run')

            else:
                print('[TwitterCam] Running ...')
                image_object = self.takePicture.takePicture()

                result = self.postOnTwitter.post(
                    self.shots[shot_to_be_run]['message'],
                    # 'Hello Twitter! ' + image_object.getTimestampCreated().strftime(self.config.getFeatureConfig('take_picture').getValue('filename_time_format')),
                    image_object,
                    in_reply_to_status_id = None
                )

                if result['error']:
                    print('FTPSUplod failed! ' + result.response)

                self.shots[shot_to_be_run]['last_execution_time'] = datetime.datetime.now()

                print('[TwitterCam] Done.')

        else:
            print('[TwitterCam] Inactive')

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
            print('[TwitterCam] ' + self.shots[i]['time_of_day'] + ':')
            lte = self.shots[i]['last_execution_time'] or 'never'
            print('[TwitterCam] > last time executed:', lte)

            if getTimeOfDayFromString(self.shots[i]['time_of_day']) <= now:
                print('[TwitterCam] > not in future')

                if getTimeOfDayFromString(self.shots[i+1]['time_of_day']) <= now:
                    print('[TwitterCam] > next shot not in future --> pass')
                    if not shotAlreadyExecutedToday(i):
                        print('[TwitterCam] > (this shot is over-due and is therefore being skipped!)')

                else:
                    print('[TwitterCam] > next shot in future')
                    if not shotAlreadyExecutedToday(i):
                        print('[TwitterCam] > not exectued today --> execute')
                        return i
                    else:
                        print('[TwitterCam] > already executed today --> no shot to run')
                        return None

            else:
                print('[TwitterCam] > in future --> pass')
                pass
