import os
import time
import datetime
# from picamera import PiCamera
import json
from TwitterAPI import TwitterAPI

import shutil

### READ CONFIG ###

with open("config.json") as json_config_file:
    CONFIG = json.load(json_config_file)


### FUNCTIONS ###

# mock function!
def take_picture():
    print("take_picture(): picture taken (mocked)")

    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    print (current_time)
    file_path = os.path.join('pictures', current_time + '.png')
    shutil.copyfile('pictures/dummy.png', file_path)
    return file_path

# def take_picture():
#     try:
#         camera = PiCamera()
#         camera.resolution = (1024, 768)
#         camera.start_preview()
#         time.sleep(2) # Give camera some time to get ready
#         camera.capture('foo.jpg')
#     except:
#         print("Error: ", sys.exc_info()[0])
#         raise
    
def upload_picture(file_path):
    print("upload_picture() not implemented yet!")

def tweet_picture(file_path):

    twitter = TwitterAPI(
        CONFIG["twitter"]["api_key"],
        CONFIG["twitter"]["api_key_secret"],
        CONFIG["twitter"]["access_token"],
        CONFIG["twitter"]["access_token_secret"]
    )

    # Request a tweet:

    print('Searching for Tweets ...')
    response = twitter.request(
        'search/tweets',
        { 'q': '#JustDevThings' }
    )
    print(response.status_code)
    
    for tweet in response.get_iterator():
        if 'text' in tweet:
            print(tweet['text'])

    # Post a tweet:

    print('Tweeting status ...')
    response = twitter.request(
        'statuses/update',
        { 'status': 'Hello World! Part 3.' }
    )
    print (response.status_code)

    # Post a picture:

    print('Tweeting picture ...')

    # step 1: upload image:
    file = open(file_path, 'rb')
    picture = file.read()
    response = twitter.request(
        'media/upload',
        None,
        { 'media': picture }
    )
    print (response.status_code)

    # step 2: tweet status with reference to uploaded picture:
    if response.status_code == 200:
        media_id = response.json()['media_id']
        response = twitter.request(
            'statuses/update',
            {
                'status': 'Hello World! This is a picture :-)',
                 'media_ids': media_id
            }
        )
        print (response.status_code)

### MAIN ###

print("Hello from Python!")

file_path = take_picture()

status = upload_picture(file_path)

status = tweet_picture(file_path)