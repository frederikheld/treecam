"""
This is a data object to store images taken by TakePictures
and pass them around. Besides the image data it contains
meta data

    * datetime.datetime | timestamp created | defaults to datetime.datetime.now()
    * String | mime type
"""

import datetime

class Image:

    def storeImage(self,
        image_bytes_object,
        mime_type,
        timestamp_created = datetime.datetime.now()
    ):
        """
            Parameter:
                image_bytes_object | BytesIO | the image
                mime_type | String | mime type of the image
                timestamp_create | datetime.datetime | timestamp of the time the image was created

            Returns:
                None
        """
        self.image_bytes_object = image_bytes_object
        self.timestamp_created = timestamp_created
        self.mime_type = mime_type

    def getImage(self):
        """
            Parameter:
                None

            Returns:
                BytesIO | image object
        """
        self.image_bytes_object.seek(0) # "rewind" BytesIO stream
        return self.image_bytes_object

    def getTimestampCreated(self):
        """
            Parameter:
                None
        
            Returns:
                datetime.datetime | timestamp
        """
        return self.timestamp_created

    def getMIMEType(self):
        """
            Paramter:
                None

            Returns:
                String | mime type
        """
        return self.mime_type
