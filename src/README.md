# Setup


## Prerequisites

On balenaCloud:

Create a balenaCloud account and log into it.

Create a new app "TreeCam".

On your computer:

Install [balenaCLI](https://github.com/balena-io/balena-cli/blob/master/INSTALL.md), [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and [Docker Engine with Docker CLI and Docker Compose](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and a tool to write SD cards like [balenaEtcher](https://www.balena.io/etcher/) or [Raspberry Pi Imager](https://www.raspberrypi.org/software/).

Use Git to clone this repository including submodules:

```sh
$ git clone --recurse-submodules https://github.com/frederikheld/treecam.git
```

Open a terminal and navigate into the `src/` directory of the repository (this directory).

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

## Setup balenaCloud

On balenaCloud:

Create new device in the previously created app "TreeCam". Follow the dialog to download balenaOS image. You can (but don't need to) specify your WiFi credentials in this dialog. If no WiFi is configured, the device will open a captive portal to configure WiFi credentials on startup.

The download will be a `zip`  file that contains an `img` file. Unzip it so that you can proceed to work with the `img` file.

## Write image to SD card

On your computer:

The previously downloaded image is an empty balenaOS image that is linked to the "TreeCam" app in your account. If you haven't configured WiFi credentials in the process, it won't even be able to pull the app from balenaCloud. This is why we are going to [preload](https://www.balena.io/docs/reference/balena-cli/#preload-image) the image before we flash it to the SD card.

Make sure you're in the `src/` directory and that you have the path where you have downloaded the balenaOS image at hand. Then preload the image:

```sh
$ balena preload /path/to/balena.img --app TreeCam --commit current
```

Now write the pre-loaded image to your SD card using an image writer software.

## Prepare SD card

At this point, please have a look into the `README.md` files of each individual service to learn how to prepare the SD card and balenaCloud for the services to run.

## Install SD card in RasPi

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

Check your router for the IP of the "TreeCam" device.

## Setup TreeCam

// tbd: instructions on how to configure "TreeCam" via the web interface