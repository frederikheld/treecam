from modules.feature.helloworld import HelloWorld
from modules.feature.takepicture import TakePicture
from modules.feature.postontwitter import PostOnTwitter
from modules.feature.ftpsupload import FTPSUpload

from modules.data.config import Config

from datetime import datetime

import json

def main():
    # testing stuff:
    hello = HelloWorld()
    hello.hello()
    hello.hello('Fred')

    # load config:
    config = Config()
    config.loadConfigFromJSONFile('config.json')
    print(config.getGlobalConfig())

    # take picture:
    takePicture = TakePicture(config.getModuleConfig('take_picture'))
    image_object = takePicture.take_picture()

    # post picture to Twitter:
    postOnTwitter = PostOnTwitter(config.getModuleConfig('post_on_twitter'))
    result = postOnTwitter.post(
        'Hello Twitter! ' + image_object.get_timestamp_created().strftime(config.getGlobalConfig('filename_time_format')),
        image_object,
        in_reply_to_status_id = None
    )

    if result['error']:
        print('PostOnTwitter failed! ' + result.respones)

    # upload to FTPS server:
    ftps_config = config.getModuleConfig('ftps_upload')
    ftps_config['filename_time_format'] = config.getGlobalConfig('filename_time_format')
    ftpsUpload = FTPSUpload(ftps_config)
    result = ftpsUpload.upload(image_object)

    # NOTE: The handling of ftps_config is just a workaround until we have a proper config data object

    if result['error']:
        print('FTPSUplod failed! ' + result.response)

main()