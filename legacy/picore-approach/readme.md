# TreeCam

// tbd

## Requirements

- Raspberry Pi \*
- RaspiCam

\* this Tutorial explains how to setup a RasPi Zero W, which already has an integrated wifi module. For other models you have to setup wifi yourself.

## Set up Raspberry Pi with PiCore Linux

Follow this tutorial: https://www.novaspirit.com/2018/01/09/tiny-core-raspberry-pi-zero-w-install/

There's also a video that covers the tutorial: https://www.youtube.com/watch?v=aKvW59uk4PY

Now you are ready to start the RasPi. All further steps assume that you access the RasPi via ssh. The standard user is _tc_ (password _piCore_), the standard hostname is _box_.

    $ ssh tc@box

## Install additional modules

TinyCore ships with `vi`. There's also a version of `nano` for TinyCore which can be installed from the app repository.

    $ tce-load -wi nano.tcz

To get TreeCam running, you need `lftp`.

    $ tce-load -wi lftp.tcz

You might also want to install `rsync` to copy files directly between the RasPi and your computer. This is not needed for TreeCam but makes setup easier.

    $ tce-load -wi rsync.tcz

You also need rsync to be installed on your computer, which already is the case in many distributions.

## Change hostname

This step is optional but giving the RasPi a catchy hostname makes it easier to find it in the network. The hostname is defined in two locations.

Fist location is _/etc/hosts_.

$ sudo nano /etc/hosts

Replace _box_ by your favorite hostname. I will use _treecam_ in this tutorial.

The second location is _/etc/hostname_ which contains nothing but the hostname.

    $ sudo nano /etc/hostname

Replace _box_ by the same hostname you used in the previous step.

Reboot the RasPi and check if you can now ssh into it with the new hostname.

## Setup RaspiCam

Install the app `rpi-videocore` to get the camera running.

    $ tce-load -wi rpi-videocore.tcz

Set access rights for the video device. To have them set at every boot, add the following line to `/opt/bootlocal.sh`.

    chmod 777 /dev/vchiq

Reboot and check if you can take a picture with `raspistill`.

    $ cd ~
    $ raspistill -o pic.jpg

To check the result, you can copy it to your computer with rsync. Run the following command on your computer.

    $ cd ~
    $ rsync tc@treecam:/home/tc/pic.jpg .

## Setup cron

To enable the cron service at startup, add the following line to `/opt/bootlocal.sh`

    cron -L /dev/null 2>&1

You also need to add the `cron` bootflag to the boot command in
