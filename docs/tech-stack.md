# Tech Stack

Year after year I started too late with this project and thus didn't finish in time for the first buds to burst.

This is the year 2021. This is another attempt to beat spring. This time based on a slightly different tech stack.

* Hardware: [RasPi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) with [Camera Module](https://www.raspberrypi.org/products/camera-module-v2/) in the [official case](https://www.raspberrypi.org/products/raspberry-pi-zero-case/) (which also houses the camera). This is a compact package that allows to mount the TreeCam with some contraption made of cardboard and sticky tape at the windown in the right angle.
* System: [balenaOS](https://www.balena.io/os/) [1] on a 4 GB MicroSD card
* Microservices running in the balenaOS Docker environment

[1] My previous attempt to satisfy requirement 4 was based on PiCore Linux. This had some drawbacks: Creating own packages for PiCore was difficult because the means were limited. For a long time PiCore didn't look like it is still under active development. And I would have needed to implement everytghing to satisfy requirement 5 by myself. After working with [balenaOS](https://www.balena.io/os/) and [balenaCloud](https://www.balena.io/cloud/) in different project, this seems to be an easier approach to achieve this.