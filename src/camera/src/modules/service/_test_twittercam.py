import pytest

import datetime

from modules.data.config import Config
from modules.service.twittercam import TwitterCam

def test_TwitterCam_isDueToRun():
    twittercam_config = Config({
        "active": True,
        "features": {
            "take_picture": {},
            "post_on_twitter": { "active": False }
        },
        "shots": [
            {
                "time_of_day": "08:00:00",
                "last_time_executed": "2021-03-01 08:01:51.227604"
            },
            {
                "time_of_day": "12:00:00",
                "last_time_executed": "2021-03-02 12:03:23.227604"
            },
            {
                "time_of_day": "16:00:00",
                "last_time_executed": None
            },
            {
                "time_of_day": "23:00:00",
                "last_time_executed": None
            }
        ]
    })

    timestamp_now = '2021-03-02 11:04:00.000000'
    twitterCam = TwitterCam(twittercam_config)
    assert twitterCam.serviceIsDueToRun(timestamp_now) == True
    assert twitterCam.shotToExecuteNext() == 0

    timestamp_now = '2021-03-02 12:04:00.000000'
    twitterCam = TwitterCam(twittercam_config)
    assert twitterCam.serviceIsDueToRun(timestamp_now) == True
    assert twitterCam.shotToExecuteNext() == 1

    timestamp_now = '2021-03-02 16:04:00.000000'
    twitterCam = TwitterCam(twittercam_config)
    assert twitterCam.serviceIsDueToRun(timestamp_now) == True
    assert twitterCam.shotToExecuteNext() == 2
