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

    response = twitter.request('search/tweets', {'q': '#JustDevThings'})
    print(response.status_code)
    
    for tweet in response.get_iterator():
        if 'text' in tweet:
            print(tweet['text'])

    # Post a tweet:

    response = twitter.request('statuses/update', {'status': 'Hello World! Part 3.'})
    print (response.status_code)


### MAIN ###

print("Hello from Python!")

take_picture()

upload_picture()

tweet_picture()