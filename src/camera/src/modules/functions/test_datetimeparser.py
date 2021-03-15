import pytest
import datetime

from contextlib import contextmanager
from unittest.mock import patch

from modules.functions.datetimeparser import *

mockDateTime = datetime.datetime(2021, 3, 21, 11, 4, 0, 123456)
# '2021-03-02 11:04:00.123456'

########################################
# Mock functions (as contextmanager)   #
########################################

@contextmanager
def mock_datetime_now(now):

    class MockDatetimeNow:
        @classmethod
        def now(cls):
            return now

    with patch('datetime.datetime', MockDatetimeNow):
        yield


########################################
# Tests                                #
########################################

def test_shotAlreadyExecutedToday():
    
    mockDatetimeNow = datetime.datetime(2021, 3, 1)
    mockDatetimeInPast = datetime.datetime(2001, 1, 1)
    mockDatetimeInFuture = datetime.datetime(2100, 3, 5)

    with mock_datetime_now(mockDatetimeNow):
        # This just checks if the mock is working correctly:
        assert datetime.datetime.now() == mockDatetimeNow
        assert datetime.datetime.now() > mockDatetimeInPast
        assert datetime.datetime.now() < mockDatetimeInFuture

        print(datetime.datetime.now().year)

        # assert shotAlreadyExecutedToday(mockDatetimeInFuture) == False


def test_isSameDay():
    # same day, A > B:
    assert isSameDay('2021-03-02 11:04:00.000000', '2021-03-02 00:04:00.123545')
    assert isSameDay('2021-03-01 11:04:00.000000', '2021-03-01 00:04:00.123545')

    # same day, A < B:
    assert isSameDay('2021-03-02 02:04:00.000000', '2021-03-02 05:04:00.123545')
    assert isSameDay('2021-03-01 11:04:00.000000', '2021-03-01 12:04:00.123545')

    # same day, A == B:
    assert isSameDay('2021-03-01 11:04:00.000000', '2021-03-01 11:04:00.000000')

    # not same day, A > B:
    assert not isSameDay('2021-06-01 11:04:00.000000', '2021-03-01 00:04:00.123545')
    assert not isSameDay('2021-03-01 23:59:59.999999', '2021-02-02 00:00:00.000000')

    # not same day, A < B:
    assert not isSameDay('2021-02-01 11:04:00.000000', '2021-03-01 00:04:00.123545')
    assert not isSameDay('2021-02-01 23:59:59.999999', '2021-02-02 00:00:00.000000')

    # returns False if at least one parameter is None:
    assert not isSameDay(None, '2021-02-01 11:04:00.000000')
    assert not isSameDay('2021-02-01 11:04:00.000000', None)
    assert not isSameDay(None, None)

# def test_datetimeIsInFuture():

#     # same day, A > B --> True:
#     assert datetimeIsInFuture('2021-03-02 11:04:00.000000', '2021-03-02 00:04:00.123545')
#     assert datetimeIsInFuture('2021-03-01 11:04:00.000000', '2021-03-01 00:04:00.123545')

#     # same day, A < B --> False:
#     assert not datetimeIsInFuture('2021-03-02 02:04:00.000000', '2021-03-02 05:04:00.123545')
#     assert not datetimeIsInFuture('2021-03-01 11:04:00.000000', '2021-03-01 12:04:00.123545')

#     # A == B --> False:
#     assert not datetimeIsInFuture('2021-03-01 11:04:00.000000', '2021-03-01 11:04:00.000000')

#     # not same day, A < B --> False:
#     assert not datetimeIsInFuture('2021-02-01 11:04:00.000000', '2021-03-01 00:04:00.123545')
#     assert not datetimeIsInFuture('2021-02-01 23:59:59.999999', '2021-02-02 00:00:00.000000')

#     # not same day, A > B --> True:
#     assert datetimeIsInFuture('2021-10-01 11:04:00.000000', '2021-03-01 00:04:00.123545')
#     assert datetimeIsInFuture('2021-12-01 23:59:59.999999', '2021-02-02 00:00:00.000000')

#     # returns False if one of the values is None:
#     assert not datetimeIsInFuture(None, '2021-10-01 11:04:00.000000')
#     assert not datetimeIsInFuture('2021-10-01 11:04:00.000000', None)
#     assert not datetimeIsInFuture(None, None)

# def test_timeIsInFuture():

#     # A > B --> True:
#     assert timeIsInFuture('11:04:00.000000', '00:04:00.123545')
#     assert timeIsInFuture('23:59:59.999999', '00:00:00.000000')

#     # A < B --> False:
#     assert not timeIsInFuture('02:04:00.000000', '05:04:00.123545')
#     assert not timeIsInFuture('11:04:00.000000', '12:04:00.123545')

#     # A == B --> False:
#     assert not timeIsInFuture('11:04:00.000000', '11:04:00.000000')

#     # returns False if one of the values is None:
#     assert not timeIsInFuture(None, '11:04:00.000000')
#     assert not timeIsInFuture('11:04:00.000000', None)
#     assert not timeIsInFuture(None, None)

def test_getTimeOfDayString():
    # extracts HH:MM:SS:
    assert getTimeOfDayString('2021-02-01 11:04:00.000000') == '11:04:00'
    assert getTimeOfDayString('2021-02-01 11:00:23.000000') == '11:00:23'

    # ignores microseconds:
    assert getTimeOfDayString('2021-02-01 11:04:00.123511') == '11:04:00'
    assert getTimeOfDayString('2022-02-01 00:04:00.312323') == '00:04:00'

def test_getTimeOfDayFromString():
    # works for full datetime.datetime string:
    assert getTimeOfDayFromString('2021-02-01 11:04:00.000000') == datetime.time(hour=11, minute=4)
    assert getTimeOfDayFromString('2021-02-01 11:00:23.000000') == datetime.time(hour=11, second=23)
    assert getTimeOfDayFromString('2021-02-01 11:04:00.123511') == datetime.time(hour=11, minute=4, microsecond=123511)
    assert getTimeOfDayFromString('2022-02-01 00:04:00.312323') == datetime.time(minute=4, microsecond=312323)

    # works for simple datetime.time string without microseconds:
    assert getTimeOfDayFromString('11:04:00') == datetime.time(hour=11, minute=4)
    assert getTimeOfDayFromString('11:00:23') == datetime.time(hour=11, second=23)
    assert getTimeOfDayFromString('00:04:00') == datetime.time(minute=4)


def test_timeDelta():

    # start < end:
    assert timeDelta('11:04:00', '11:04:01') == 1
    assert timeDelta('11:04:00', '11:05:00') == 60
    assert timeDelta('11:04:00', '12:04:00') == 3600

    # start > end:
    assert timeDelta('11:04:01', '11:04:00') == -1
    assert timeDelta('11:05:00', '11:04:00') == -60
    assert timeDelta('12:04:00', '11:04:00') == -3600

    # start == end:
    assert timeDelta('11:04:00', '11:04:00') == 0

    # start = midnight:
    assert timeDelta('00:00:00', '01:00:00') == 3600

    # end = midnight:
    assert timeDelta('01:00:00', '00:00:00') == -3600
