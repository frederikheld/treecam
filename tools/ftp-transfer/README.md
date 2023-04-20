# FTP Transfer

This tool automates the archiving of pictures on a local computer after they were uploaded to an FTP server by the cam.

## shell script

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

## Docker container

There also is a Docker container that you can use to run the script.

The notable difference to the script file is that it already schedules a cronjob _within_ the container to run the transfer script periodically.

So all you have to do is build the container and then run it with the necessary environment vars passed into it.

Please note that with the Docker setup, the `ARCHIVE_DIR` will not be passed as an env variable but be mounted as a bind mount from the local file system to the container's `/out` directory.

```sh
docker build -t treecam-transfer-tool .
docker run -d --name treecam-transfer-tool -env FTP_SERVER='my.server.example' -env FTP_DIR='upload-dir' --env FTP_USER='username' --env FTP_SECRET='secret' --volume /archive-dir:/out treecam-transfer-tool
```

Instead of providing each individual environment variable via `--env`, you can use `--env-file .env` to provide the variables from an `.env` file instead.
