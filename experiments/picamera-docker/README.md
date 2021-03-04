# Run PiCamera in Docker container

This is a test to run PiCamera in a Docker container on Raspberry Pi OS.

> Note: This version is to be run standalone with the original Docker engine. It is not designed to run with balenaOS!


It is following these tutorials and hints:

* https://www.losant.com/blog/how-to-access-the-raspberry-pi-camera-in-docker
* https://forums.balena.io/t/picamera-not-working-as-expected/5672

## Prep

In order to get it running, prepare the following:

* enable the camera interface via `raspi-config`
* enable camera for `docker` user via `udev` [source](https://www.losant.com/blog/how-to-access-the-raspberry-pi-camera-in-docker)

For balenOS, some things need to be done different:

* to set the `udev` rule, add `"SUBSYSTEM==\"vchiq\",MODE=\"0666\"\n"` to `config.json`  (via `config.json` on resin-boot partition of the balenaOS SD card) [source1](https://github.com/balena-os/meta-balena#udevrules) [source2](https://github.com/balena-os/meta-balena/pull/1206)
* set fleet variables `BALENA_HOST_CONFIG_gpu_mem_512 256` and `BALENA_HOST_CONFIG_start_x 1` in balenaCloud OR defined `gpu_mem_512=256` and `start_x=1` in `config.txt` on resin-boot partition of balenaOS SD card.


## Build & Run

### Without `docker-compose`

Build:

```sh
$ sudo docker build --tag treecam-experiment .
```

Run:

```sh
$ sudo docker run --device=/dev/vcsm-cma --device=/dev/vchiq -v /opt/vc:/opt/vc -v $(pwd)/scripts:/usr/src/app --env LD_LIBRARY_PATH=/opt/vc/lib --name treecam-experiment --rm treecam-experiment
```

> Note: `$(pwd)` is being mounted to `/usr/src/app` to be able to update the scripts without the need to re-build the container during development and to have access to the picture that was taken. This can later be replaced by the `COPY` command in the `Dockerfile`!
