import pytest
import datetime
import logging

from modules.data.config import Config
from modules.service.timercam import TimerCam

def test_run_service_inactive(caplog):

    config = Config({
        'active': False,
        'features': {
            'take_picture': { 'active': True },
            'ftps_upload': { 'active': False }
        }
    })

    with caplog.at_level(logging.DEBUG):
        timerCam = TimerCam(config)
        result = timerCam.run(datetime.datetime(year=2001, month=1, day=1))

    assert result == True
    assert 'Inactive' in caplog.text

def test_run_service_active(caplog):

    config = Config({
        'active': True,
        'features': {
            'take_picture': { 'active': True },
            'ftps_upload': { 'active': False }
        }
    })

    with caplog.at_level(logging.DEBUG):
        timerCam = TimerCam(config)
        result = timerCam.run(datetime.datetime(year=2001, month=1, day=1))

    assert result == True
    assert 'Running' in caplog.text
    assert 'Done' in caplog.text

def test_run_provider_inactive(caplog):
    """
    Service will be aborted if no image provider is active.
    """

    config = Config({
        'active': True,
        'features': {
            'take_picture': { 'active': False },
            'ftps_upload': { 'active': False }
        }
    })

    with caplog.at_level(logging.DEBUG):
        timerCam = TimerCam(config)
        result = timerCam.run(datetime.datetime(year=2001, month=1, day=1))

    assert result == False
    assert 'take_picture is inactive' in caplog.text
    assert 'aborted' in caplog.text

def test_run_ftps_upload_inactive(caplog):

    config = Config({
        'active': True,
        'features': {
            'take_picture': { 'active': True },
            'ftps_upload': { 'active': False }
        }
    })

    with caplog.at_level(logging.DEBUG):
        timerCam = TimerCam(config)
        result = timerCam.run(datetime.datetime(year=2001, month=1, day=1))

    assert result == True
    assert 'ftps_upload is inactive' in caplog.text
    assert 'Done' in caplog.text

# test: serviceIsDueToRun()