"""
TreeCam feature FTPSUpload
"""

import os
import datetime
import ftplib

class FTPSUpload:

    def __init__(self, config_dict):
        self.config = config_dict

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
                self.config["url"],
                21
            )
            print("connect > " + response)

            resonse = ftp.login(
                self.config["user"],
                self.config["secret"]
            )
            print("login > " + response)

            response = ftp.prot_p() # ask for secure data connection
            print("protection > " + response)

            ftp.cwd('/upload')

            ftp_command = "STOR " + image_object.get_timestamp_created().strftime(self.config['filename_time_format']) + '.' + image_object.get_mime_type()
            print(ftp_command)

            response = ftp.storbinary(
                ftp_command,
                image_object.get_image()
            )
            print("upload > " + response)

            ftp.dir() # DEBUG

        return { "error": False }
