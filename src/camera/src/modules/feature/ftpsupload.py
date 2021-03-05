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
        # if not "ftps_upload" in CONFIG["timer_cam"]:
        #     return {
        #         error: True,
        #         response: 'ftps_upload not configured'
        #     }

        # if not self.config["active"]:
        #     return {
        #         error: True,
        #         response: 'ftps_upload not configured'
        #     }

        self.logger.info("initializing FTP upload")
        with ftplib.FTP_TLS() as ftp:
            ftp.encoding = 'utf-8'

            try:
                response = ftp.connect(
                    self.config.getValue("url"),
                    self.config.getValue("port")
                )
                self.logger.info("connect > " + response)

                resonse = ftp.login(
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

            except Exception as error:
                self.logger.warn('Could not connect to FTPS server at ' + self.config.getValue('url') + ':' + str(self.config.getValue('port')) + ': ' + str(error))

        return { "error": False }
        # TODO: return True instead of dict here! This is not JS!
