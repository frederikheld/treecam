"""
TreeCam feature PostOnTwitter
"""

import logging

from TwitterAPI import TwitterConnectionError
from TwitterAPI import TwitterAPI

class PostOnTwitter:

    def __init__(self, config_object):
        """
        Parameters:
            config_object | Config object | Module-specific configuration
        """

        self.config = config_object

        self.logger = logging.getLogger(__name__)

        self.twitterAPI = TwitterAPI(
            self.config.getValue("secrets")["api_key"],
            self.config.getValue("secrets")["api_key_secret"],
            self.config.getValue("secrets")["access_token"],
            self.config.getValue("secrets")["access_token_secret"]
        )
        self.twitterAPI.REST_TIMEOUT = self.config.getValue('timeout') or 5

    def post(
        self,
        status_message,
        image_object = None,
        in_reply_to_status_id = None):

        """
        Posts on Twitter

        Parameters:
        * Posts the `status_message` as a tweet on Twitter.
        * If the optional `image_object` is given, it will include this image in the tweet.
        * You can also provide the optional `in_reply_to_status_id` to post the tweet as
          a reply to a tweet you posted before.

        Return value:
        This method returns a dict with two keys `error` and `response`.
        `error` is False if successfully tweeted. Otherwise True.
        `response` contains the response object from the Twitter API (see [1] for details).
        
        [1]: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/post-statuses-update
        """

        media_id = None
    
        if image_object:
            try:
                response = self.twitterAPI.request(
                    'media/upload',
                    None,
                    { 'media': image_object.getImage() }
                )

                if response.status_code != 200:
                    return {
                        'error': True,
                        'response': response.json()
                    }

                media_id = response.json()['media_id']

                try:
                    response = self.twitterAPI.request(
                        'statuses/update',
                        {
                            'status': status_message,
                            'media_ids': media_id,
                            'in_reply_to_status_id': in_reply_to_status_id
                        }
                    )

                except TwitterConnectionError:
                    error_message = 'Could not connect to Twitter API within ' + str(self.twitterAPI.REST_TIMEOUT) + ' seconds while trying to post the message!'

                    raise ConnectionError(error_message)

            except TwitterConnectionError:
                error_message = 'Could not connect to Twitter API within ' + str(self.twitterAPI.REST_TIMEOUT) + ' seconds while trying to upload the image!'

                raise ConnectionError(error_message)
