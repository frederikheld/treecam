import datetime

DATETIME_STRING_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
TIME_STRING_FORMAT = '%H:%M:%S'

def isSameDay(datetime_string_1, datetime_string_2):
    if datetime_string_1 == None or datetime_string_2 == None:
        return False

    datetime_1 = datetime.datetime.strptime(datetime_string_1, DATETIME_STRING_FORMAT).date()
    datetime_2 = datetime.datetime.strptime(datetime_string_2, DATETIME_STRING_FORMAT).date()

    return datetime_1 == datetime_2


# def datetimeIsInFuture(datetime_string_probe, datetime_string_now=datetime.datetime.now()):
#     """
#     Checks if `datetime_string_probe` is in future compared to
#     `datetime_string_now`.
#     """
#     if datetime_string_probe == None or datetime_string_now == None:
#         return False

#     datetime_now = datetime.datetime.strptime(datetime_string_now, DATETIME_STRING_FORMAT)
#     datetime_future = datetime.datetime.strptime(datetime_string_probe, DATETIME_STRING_FORMAT)

#     return datetime_now < datetime_future


# def timeIsInFuture(time_string_probe, time_string_now=datetime.datetime.now().strftime(TIME_STRING_FORMAT)):
#     """
#     Checks if `time_string_probe` is in future compared to
#     `datetime_string_now`.
#     """
#     if time_string_probe == None or time_string_now == None:
#         return False
    
#     time_now = datetime.datetime.strptime(time_string_now, TIME_STRING_FORMAT)
#     time_future = datetime.datetime.strptime(time_string_probe, TIME_STRING_FORMAT)

#     print(time_now, time_future)

#     return time_now < time_future

def getTimeOfDayFromString(datetime_string):
    try:
        datetime_object = datetime.datetime.strptime(datetime_string, DATETIME_STRING_FORMAT)
    except(ValueError):
        datetime_object = datetime.datetime.strptime(datetime_string, TIME_STRING_FORMAT)

    return datetime_object.time()

def getTimeOfDayString(datetime_string):
    datetime_object = datetime.datetime.strptime(datetime_string, DATETIME_STRING_FORMAT)

    return datetime_object.time().strftime(TIME_STRING_FORMAT)

def timeDelta(start_time_string, end_time_string):
    start_time = datetime.datetime.strptime(start_time_string, TIME_STRING_FORMAT)
    end_time = datetime.datetime.strptime(end_time_string, TIME_STRING_FORMAT)

    return datetime.timedelta.total_seconds(end_time - start_time)
