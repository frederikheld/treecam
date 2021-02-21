# TreeCam

Right in front of my window there's this wonderful tree which guides me through the seasons of the year.

In spring I eagerly await the burst of the first buds which will soon cover the whole tree in fresh green.

![This picture was taken right before the buds bursted](img/tree_right_before_spring.jpg)

In summer it provides shade during the afternoon with a great sundown after the sun shows up on it's right hand side again. It also and hums from all the bees and insects that live from it's juces.

In autumn it is my scale to see how the days get shorter every day until the sun doesn't show up on it's right hand side anymore but sets behind it. Leaves are falling and create a mess on the street below it.

In winter it is just there. Empty and naked, sometimes covered in snow. Waiting for the spring that makes it juices flow again.

Year after year I think how great it would be to follow this noble tree through the year by taking one picture every day.

## Features

### Basic features

1. Automatically take pictures (once a day, maybe even once a hour)
2. Automatically upload the pictures to an FTP server, NAS or some other safe place
3. Automatically post to Twitter (once a day? Mabye make on thread per day with one picture per time of day each?)
4. Robust system. Sudden power outages shuld not damage the device. With power restored it should get back in operating mode without any user interaction required.

### Nice to have

5. Remote access to update, fix issues, etc.
6. Setup of camera via live stream / web portal
7. Setup of wifi via captive portal
8. Setup of FTP via web portal / app
9. Setup of Twitter via web portal / app

Year after year I start too late and never finish because the buds burst quicker than I make progress.

## Tech Stack

This is the year 2021. This is another attempt to beat spring. This time based on a slightly different tech stack.

* Hardware: [RasPi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) with [Camera Module](https://www.raspberrypi.org/products/camera-module-v2/) in the [official case](https://www.raspberrypi.org/products/raspberry-pi-zero-case/) (which also houses the camera). This is a compact package that allows to mount the TreeCam with some contraption made of cardboard and sticky tape at the windown in the right angle.
* System: [balenaOS](https://www.balena.io/os/) [1] on a 4 GB MicroSD card
* Microservices running in the balenaOS Docker environment

[1] My previous attempt to satisfy requirement 4 was based on PiCore Linux. This had some drawbacks: Creating own packages for PiCore was difficult because the means were limited. For a long time PiCore didn't look like it is still under active development. And I would have needed to implement everytghing to satisfy requirement 5 by myself. After working with [balenaOS](https://www.balena.io/os/) and [balenaCloud](https://www.balena.io/cloud/) in different project, this seems to be an easier approach to achieve this.

## Prerequisites

On balenaCloud:

Create a balenaCloud account and log into it.

Create a new app "TreeCam".

On your computer:

Install [balenaCLI](https://github.com/balena-io/balena-cli/blob/master/INSTALL.md), [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and [Docker Engine with Docker CLI and Docker Compose](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and a tool to write SD cards like [balenaEtcher](https://www.balena.io/etcher/) or [Raspberry Pi Imager](https://www.raspberrypi.org/software/).

Use Git to clone this repository.

Open a terminal and navigate into the `src/` directory of the repository.

[Login to balenaCloud](https://www.balena.io/docs/reference/balena-cli/#login):

```sh
$ balena login
```

This will provide several different authentication methods. Web authorization is the simplest to use.

Check if your app is available:

```sh
$ balena apps
```

This should list your previously created "TreeCam" app.

Make sure you're in the `src/` directory. Then push the app from your local repo into the cloud:

```sh
$ balena push TreeCam
```

## Device Setup

On balenaCloud:

Create new device in the previously created app "TreeCam". Follow the dialog to download balenaOS image. You can (but don't need to) specify your WiFi credentials in this dialog. If no WiFi is configured, the device will open a captive portal to configure WiFi credentials on startup.

The download will be a `zip`  file that contains an `img` file. Unzip it so that you can proceed to work with the `img` file.

On your computer:

The previously downloaded image is an empty balenaOS image that is linked to the "TreeCam" app in your account. If you haven't configured WiFi credentials in the process, it won't even be able to pull the app from balenaCloud. This is why we are going to [preload](https://www.balena.io/docs/reference/balena-cli/#preload-image) the image before we flash it to the SD card.

Make sure you're in the `src/` directory and that you have the path where you have downloaded the balenaOS image at hand. Then preload the image:

```sh
$ balena preload /path/to/balena.img --app TreeCam --commit current
```

Now write the pre-loaded image to your SD card using an image writer software.

Now put the SD card into your RasPi Zero W.

Make sure that SD card and camera ribbon cable are correctly in place.

> This is the point where the TreeCam device is ready in case you want to give it away to someone else. Everything what comes next can be done by the average user (if you point them to this tutorial).

## First Start

Connect the device with a USB power source. It will start to boot up.

On your computer or mobile phone:

Search for the WiFi `treecam`. It might take some minutes to show up. Connect your device to it.

It will redirect you to a captive portal where you can configure the credentials for the WiFi that will connect the TreeCam device to the internet. If you aren't redirected automatically, open a web browser and navigate to `192.168.3.1`.

Select your home WiFi from the list and provide your WiFi password. Save it.

The device will now shut down the `treecam` WiFi hotspot and connect to your home WiFi instead.

Connect your computer or mobile phone to your home WiFi as well.

