from time import sleep
# from picamera import PiCamera
import json
from TwitterAPI import TwitterAPI

### READ CONFIG ###

with open("config.json") as json_config_file:
    CONFIG = json.load(json_config_file)


### FUNCTIONS ###

def take_picture():
    print("take_picture(): picture taken (mocked)")

# def take_picture():
#     try:
#         camera = PiCamera()
#         camera.resolution = (1024, 768)
#         camera.start_preview()
#         sleep(2) # Give camera some time to get ready
#         camera.capture('foo.jpg')
#     except:
#         print("Error: ", sys.exc_info()[0])
#         raise
    
def upload_picture():
    print("upload_picture() not implemented yet!")

def tweet_picture():

    twitter = TwitterAPI(
        CONFIG["twitter"]["api_key"],
        CONFIG["twitter"]["api_key_secret"],
        CONFIG["twitter"]["access_token"],
        CONFIG["twitter"]["access_token_secret"]
    )

    # Request a tweet:

    print('Searching for Tweets ...')
    response = twitter.request('search/tweets', {'q': '#JustDevThings'})
    print(response.status_code)
    
    for tweet in response.get_iterator():
        if 'text' in tweet:
            print(tweet['text'])

    # Post a tweet:

    print('Tweeting status ...')
    response = twitter.request('statuses/update', {'status': 'Hello World! Part 3.'})
    print (response.status_code)

    # Post picture:

    print('Tweeting picture ...')

    # step 1: upload image:
    file = open('pictures/dummy.png', 'rb')
    picture = file.read()
    response = twitter.request('media/upload', None, {'media': picture})
    print (response.status_code)

    # step 2: tweet status with reference to uploaded picture:
    if response.status_code == 200:
        media_id = response.json()['media_id']
        response = twitter.request('statuses/update', {'status': 'Hello World! This is a picture :-)', 'media_ids': media_id})
        print (response.status_code)

### MAIN ###

print("Hello from Python!")

take_picture()

upload_picture()

tweet_picture()