"""
TreeCam feature FTPSUpload
"""

import os
import logging
import datetime
import ftplib

class FTPSUpload:

    def __init__(self, config_object):
        """
        Parameters:
            config_object | Config object | Module-specific configuration
        """
        self.config = config_object

        self.logger = logging.getLogger(__name__)

    def upload(self, image_object):

        self.logger.info("initializing FTP upload")

        try:
            with ftplib.FTP_TLS() as ftp:
                ftp.encoding = 'utf-8'

                response = ftp.connect(
                    self.config.getValue("url"),
                    self.config.getValue("port")
                )
                self.logger.info("connect > " + response)

                response = ftp.login(
                    self.config.getValue("user"),
                    self.config.getValue("secret")
                )
                self.logger.info("login > " + response)

                response = ftp.prot_p() # ask for secure data connection
                self.logger.info("protection > " + response)

                ftp.cwd(self.config.getValue('upload_dir'))

                ftp_command = "STOR " + image_object.getTimestampCreated().strftime(self.config.getValue('filename_time_format')) + '.' + image_object.getMIMEType()
                self.logger.info(ftp_command)

                response = ftp.storbinary(
                    ftp_command,
                    image_object.getImage()
                )
                self.logger.info("upload > " + response)

        except:
            raise
        
        return True
