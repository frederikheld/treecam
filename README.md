# TreeCam

Right in front of my window there's this wonderful tree which accompanies me through the seasons of the year. Year after year I think how great it would be to follow this noble tree through the year by taking pictures of it's day by day transformation.

![This picture was taken right before the buds bursted in 2021](img/tree_right_before_spring.jpg)

So I developed _TreeCam_, which takes pictures of the tree in regular intervals and posts them on Twitter as well as uploads them to a FTP server.

This repository contains the software that you can use to set up your own _TreeCam_. It also comes with a reference implementation that shows how a _TreeCam_ hardware can look like.

## Reference Implementation

You can see the latest picture that my _TreeCam_ device has taken at [treecam.frederikheld.de](https://treecam.frederikheld.de).

<s>My _TreeCam_ device is posting pictures to [twitter.com/fhdevlab](https://twitter.com/fhdevlab) automatically four times a day. I will also tweet [timelapses](https://twitter.com/search?q=%40fhdevlab%20%23timelapse) and background information from time to time.</s> Unfortunately [not anymore](https://techcrunch.com/2023/02/01/twitter-to-end-free-access-to-its-api/).

If you are interested in the hardware I'm running, please have a look into the [`./birdhouse`](./birdhouse) directory.

## Outline of the TreeCam services

_TreeCam_ is designed to run on a [_balenaOS_](https://www.balena.io/os/) powered [_Raspberry Pi_](https://www.raspberrypi.org/), which makes it resilient against sudden power outages and also allows to run updates remotely via [_balenaCloud_](https://www.balena.io/cloud). _TreeCam_ consists of different services that can be found in the subdirectories of [`./src`](./src).

### Camera

The [camera](./src/camera/README.md) service is the main service of _TreeCam_. It takes pictures and posts them to Twitter and/or an FTP server and therefore requires a RasPi camera module.

Additional services are integrated via Git submodules:

### Heating and Ventilation

[balena-hvac](https://github.com/frederikheld/balena-hvac/) is useful if you operate your camera outdoors and want to prevent damages through over-heating or condensation. It requires additional hardware!

### Convenient WiFi setup

[wifi-connect](https://github.com/balena-os/wifi-connect/) and [balena-reset](https://github.com/frederikheld/balena-reset/) can be used to manage the WiFi connection between the _TreeCam_ and your home wifi via a captive portal and reset button. You don't need those services if you provide your WiFi credentials when downloading the image in _balenaCloud_ or if you only want to use wired networking.

### Configuration

The configuration of the whole installment is done (as usual for [balena multi-container apps](https://www.balena.io/docs/learn/develop/multicontainer/)) in the [`./docker-compose.yml`](./docker-compose.yml) file in the root level of this repository. The individual configuration of each services works slightly different. Please read the `README.md` files of each service to learn about it. Each service also comes with their own exemplary `docker-compose.yml` that you can use as templates.

## Robust and user-friendly

_TreeCam_ was designed with robustness and usability in mind, which led to the following design decisions:

* The operating system is [_balenaOS_](https://www.balena.io/os/) which runs the different modules in Docker containers. It is very resilient against unexpected power loss and can be updated and maintained via [_balenaCloud_](https://www.balena.io/cloud).

* This makes it easy to operate the device in places that are difficult to access. As long as there's a WiFi connection available, you're fine

* The WiFi connection can be set up via a captive portal

* The services can easily be configured via a central _docker-compose_ file and the _balenaCloud_

* New features and services can be added with moderate Python skills

## Setup

See [src/README.md](src/README.md) for instructions how to setup your _TreeCam_ device.

## Known Issues

The [_RasPi Zero W_](https://www.raspberrypi.com/products/raspberry-pi-zero-w/) would be the perfect device for this project because of it's low price and power consumption. Unfortunately downloading the containers from the balenaCloud will most likely fail on a low-spec device like the Zero due an issue with the balenaOS watchdog. See the related support thread here: https://forums.balena.io/t/persistent-failed-to-download-image-due-to-connect-econnrefused-var-run-balena-engine-sock-error/114001/14

## Contribute

I'd be happy to receive pull requests that add new features and services to _TreeCam_. For example features that upload pictures to other social media platforms or services that implement new use cases.

Please have a look into the [issues on GitHub](https://github.com/frederikheld/treecam/issues) to see what else is planned that you could support with your skills and time.
