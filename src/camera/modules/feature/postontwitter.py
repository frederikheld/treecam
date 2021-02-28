"""
TreeCam feature PostOnTwitter
"""

from TwitterAPI import TwitterAPI

class PostOnTwitter:

    def __init__(self, config_object):
        """
        Parameters:
            config_object | Config object | Module-specific configuration
        """

        self.config = config_object

        self.twitter_api = TwitterAPI(
            self.config.getValue("secrets")["api_key"],
            self.config.getValue("secrets")["api_key_secret"],
            self.config.getValue("secrets")["access_token"],
            self.config.getValue("secrets")["access_token_secret"]
        )

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
            response = self.twitter_api.request(
                'media/upload',
                None,
                { 'media': image_object.get_image() }
            )

            if response.status_code != 200:
                return {
                    'error': True,
                    'response': response.json()
                }

            media_id = response.json()['media_id']
        
        response = self.twitter_api.request(
            'statuses/update',
            {
                'status': status_message,
                'media_ids': media_id,
                'in_reply_to_status_id': in_reply_to_status_id
            }
        )
        
        return {
            'error': response.status_code != 200,
            'response': response.json()
        }
