# Setup

## Install tooling and clone repo

On your computer:

Install [balenaCLI](https://github.com/balena-io/balena-cli/blob/master/INSTALL.md), [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and [Docker Engine with Docker CLI and Docker Compose](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and a tool to write SD cards like [balenaEtcher](https://www.balena.io/etcher/) or [Raspberry Pi Imager](https://www.raspberrypi.org/software/).

Use Git to clone this repository including submodules:

```sh
$ git clone --recurse-submodules https://github.com/frederikheld/treecam.git
```

Open a terminal and navigate into the `src/` directory of the repository (the directory where this README file is located).

## Configure TreeCam

At this point, please have a look into the `README.md` files of each individual service to learn how to configure the individual _TreeCam_ services.

## Setup balenaCloud

On balenaCloud:

Create a [balenaCloud](https://www.balena.io/cloud/) account and log into it.

Create a new app "TreeCam".

On our computer:

Login to balenaCloud on your terminal:

```sh
$ balena login
```

This will provide you with several different authentication methods. Web authorization is the simplest to use. Follow the instructions on the screen.

Check if your app is available:

```sh
$ balena apps
```

This should list your previously created "TreeCam" app.

Make sure you're in the `src/` directory. Then push the app from your local repo into the cloud:

```sh
$ balena push TreeCam
```

## Prepare SD card

On balenaCloud:

Create a new device in the previously created app "TreeCam". Follow the dialog to download a balenaOS image. You can (but don't need to) specify your WiFi credentials in this dialog. If no WiFi is configured, the device will open a captive portal to configure WiFi credentials on startup.

On your computer:

The download will be a `zip` file that contains an `img` file. Unzip it so that you can work with the `img` file.

The image is an empty balenaOS image that is linked to the "TreeCam" app in your account. If you haven't configured WiFi credentials in the process, it won't even be able to pull the app from balenaCloud. This is why we are going to [preload](https://www.balena.io/docs/reference/balena-cli/#preload-image) the image before we flash it to the SD card.

Make sure you're in the `src/` directory and that you have the path where you have downloaded the balenaOS image at hand. Then preload the image:

```sh
$ balena preload /path/to/balena.img --app TreeCam --commit current
```

Now write the pre-loaded image to your SD card using an image writer software.

## Install SD card in RasPi

Now put the SD card into your RasPi Zero W.

Make sure that SD card and camera ribbon cable are correctly in place.

> This is the point where the TreeCam device is preapared for it's first start. This would be the condition in which you could give it away to users that do not have development skills. Everything what comes next can be done by the average user.

## First Start

Connect the device to an USB power source. It will start to boot up and indicate with a blink pattern (4 blinks in a row) of the green activity indicator that it is ready. It might take a couple of minutes to get there!

On your computer or mobile phone:

Search for the WiFi `treecam` and connect your device to it.

It will redirect you to a captive portal where you can configure the credentials for the WiFi that will connect the TreeCam device to the internet. If you aren't redirected automatically, open a web browser and navigate to `192.168.3.1`.

Select your home WiFi from the list and provide your WiFi password. Save it.

The device will now shut down the `treecam` WiFi hotspot and connect to your home WiFi instead.

Connect your computer or mobile phone to your home WiFi as well.

## Setup TreeCam

> It is planned to add a web interface to configure _TreeCam_ interactively. This will be the replacement for the `config.json` configuration explained above.

<!-- Check your router for the IP of the "TreeCam" device. -->
