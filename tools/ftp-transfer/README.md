# FTP Transfer

This repository is an addition to the [TreeCam](https://github.com/frederikheld/treecam) project. It automates the archiving of pictures that were uploaded to an FTP server by the cam.

You can use the `transfer.sh` script to transfer the pictures from the FTP server to your local computer/server/NAS. The script will file the pictures into daily subfolders and then delete the archived pictures from the FTP server to make space.

Before you run the script, you have to export the following environment variables:
```sh
FTP_SERVER
FTP_DIR
FTP_USER
FTP_SECRET
ARCHIVE_DIR
```

`ARCHIVE_DIR` is the directory to which the pictures shall be moved after they are downloaded. The script will sort them into sub-directories by date.

> Please note that the `ARCHIVE_DIR` has to be an existing and writable directory! The script will not try to create this directory if it does not exist to prevent having directories created in unexpected places if the setting is incorrect.

Now run the script with

```sh
sh transfer.sh
```

You can also put the environment variables into an `.env` file. The script will look for this file and automatically load the variables from the file if it exists. This will overwrite variables that were previously set! This repository comes with an template for this file called `.env.template` which you can rename to `.env` and fill in your settings.
