import pytest
import datetime
import logging

# from mock import patch

from modules.data.config import Config
from modules.service.twittercam import TwitterCam

configDict = {
    'active': False,
    'features': {
        'take_picture': { 'active': True },
        'post_on_twitter': {
            'active': False,
            'secrets': {
                'api_key': 'wasdwasd',
                'api_key_secret': 'wasdwasd',
                'access_token': 'wasdwasd',
                'access_token_secret': 'wasdwasd'
            }
        }
    },
    'shots': [
        {
            "time_of_day": str(datetime.datetime.now() - datetime.timedelta(minutes=5)),
            "message": "Good morning!"
        }
    ]
}

def test_run_service_inactive(caplog):

    configDict['active'] = False
    config = Config(configDict)

    with caplog.at_level(logging.DEBUG):
        twitterCam = TwitterCam(config)
        result = twitterCam.run(datetime.datetime.now())

    assert result == True
    assert 'Inactive' in caplog.text

def test_run_service_active(caplog):

    configDict['active'] = True
    config = Config(configDict)

    with caplog.at_level(logging.DEBUG):
        twitterCam = TwitterCam(config)
        result = twitterCam.run(datetime.datetime.now())

    assert result == True
    assert 'Running' in caplog.text
    assert 'Done' in caplog.text

# CONTINUE: how to mock out PostOnTwitter.post()?

# @patch.object(PostOnTwitter, 'post')
# def test_run_provider_inactive(caplog):
#     """
#     Service will be aborted if no image provider is active.
#     """

#     configDict['features']['take_picture']['active'] = False
#     config = Config(configDict)

#     with caplog.at_level(logging.DEBUG):
#         twitterCam = TwitterCam(config)
#         result = twitterCam.run(datetime.datetime.now())

#     assert result == False
#     assert 'take_picture is inactive' in caplog.text
#     assert 'aborted' in caplog.text

# def test_run_post_on_twitter_inactive(caplog):

#     config = Config({
#         'active': True,
#         'features': {
#             'take_picture': { 'active': True },
#             'post_on_twitter': { 'active': False }
#         }
#     })

#     with caplog.at_level(logging.DEBUG):
#         twitterCam = TwitterCam(config)
#         result = twitterCam.run(datetime.datetime(year=2001, month=1, day=1))

#     assert result == True
#     assert 'post_on_twitter is inactive' in caplog.text
#     assert 'Done' in caplog.text

# test: serviceIsDueToRun()
