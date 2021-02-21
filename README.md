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