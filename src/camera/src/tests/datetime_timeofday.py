import datetime

last_execution_time = datetime.datetime.now()

print (last_execution_time)

last_execution_time = last_execution_time - datetime.timedelta(minutes=500)

print(last_execution_time)

# last_execution_time = last_execution_time - datetime.timedelta(days=1, minutes=2)

# print(last_execution_time)

last_execution_time_of_day = datetime.time(last_execution_time.hour, last_execution_time.minute, last_execution_time.second)

print(last_execution_time_of_day)

current_datetime = datetime.datetime.now()
current_time_of_day = datetime.time(current_datetime.hour, current_datetime.minute, current_datetime.second)

print(current_time_of_day)

print(current_time_of_day > last_execution_time_of_day)

for i in range(len(['1', '2', '3'])):
    print(i)

print(datetime.datetime.now())