"""
TreeCam feature FTPSUpload
"""

import os
import datetime
import ftplib

class FTPSUpload:

    def __init__(self, config_object):
        """
        Parameters:
            config_object | Config object | Module-specific configuration
        """
        self.config = config_object

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

        print ("initializing FTP upload")
        with ftplib.FTP_TLS() as ftp:
            ftp.encoding = 'utf-8'

            response = ftp.connect(
                self.config.getValue("url"),
                21
            )
            print("connect > " + response)

            resonse = ftp.login(
                self.config.getValue("user"),
                self.config.getValue("secret")
            )
            print("login > " + response)

            response = ftp.prot_p() # ask for secure data connection
            print("protection > " + response)

            ftp.cwd(self.config.getValue('upload_dir'))

            ftp_command = "STOR " + image_object.getTimestampCreated().strftime(self.config.getValue('filename_time_format')) + '.' + image_object.getMIMEType()
            print(ftp_command)

            response = ftp.storbinary(
                ftp_command,
                image_object.getImage()
            )
            print("upload > " + response)

            ftp.dir() # DEBUG

        return { "error": False }
