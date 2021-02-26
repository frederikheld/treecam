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

def tweet_picture(file_path, status, in_reply_to_status_id = None):
    """
        This function can tweet a picture with a status message.

        arguments:
            file_path: path to the picture that shall be tweeted
            status: status text of the tweet
            in_reply_to_status_id: (optional) status_id of a tweet to which this tweet will be a response

        The function returns a json object with the keys 'error' and 'response'.
            'error': False if successfully tweeted. Otherwise True.
            'response': json representation of Twitter API response object [1]

        [1]: see: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/post-statuses-update

    """

    twitter = TwitterAPI(
        CONFIG["twitter_cam"]["secrets"]["api_key"],
        CONFIG["twitter_cam"]["secrets"]["api_key_secret"],
        CONFIG["twitter_cam"]["secrets"]["access_token"],
        CONFIG["twitter_cam"]["secrets"]["access_token_secret"]
    )

    # upload image:

    file = open(file_path, 'rb')
    picture = file.read()

    response = twitter.request(
        'media/upload',
        None,
        { 'media': picture }
    )

    if response.status_code != 200:
        return {
            'error': True,
            'response': response.json()
        }

    # tweet status with reference to uploaded picture:

    media_id = response.json()['media_id']

    response = twitter.request(
        'statuses/update',
        {
            'status': status,
            'media_ids': media_id,
            'in_reply_to_status_id': in_reply_to_status_id
        }
    )
    
    return {
        'error': response.status_code != 200,
        'response': response.json()
    }

def twitter_experiments():

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


### MAIN ###

print("Hello from Python!")

file_path = take_picture()

status = upload_picture(file_path)

status = tweet_picture(file_path, 'Original image tweet')
print(status)
if status["error"]:
    print("Error: ", status["response"]["errors"])
    exit()
print(status["response"]["id"])

status = tweet_picture(file_path, 'Reply image tweet 1', status["response"]["id"])
if status["error"]:
    print("Error: ", status["response"]["errors"])
    exit()
print(status["response"]["id"])

status = tweet_picture(file_path, 'Reply image tweet 2', status["response"]["id"])
if status["error"]:
    print("Error: ", status["response"]["errors"])
    exit()
print(status["response"]["id"])

#twitter_experiments()