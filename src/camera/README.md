# Camera service

The _camera_ service is the main service of _TreeCam_. It takes pictures and posts them to different outlets. It is built in a modular way that allows to create sub-services by plugging different features together. The sub-services are registered with a service runner that takes care of execution at the expected times.

> Note: the term _service_ in the context of balenaOS describes one Docker container that is running software that serves a certain purpose. In this case it is the _camera_ service. In the context of the _camera_ service, we will use the term _service_ to describe the different sub-services that each serve a certain purpose within the _camera_ service.

## Services

The services can be configured via the common configuration file `config.json`. This repository comes with a `config.json_template`, which you can rename to `config.json`. It comes with a default configuration which you can adapt to your own needs.

> Note: You'll find detailed documentation of the `config.json` further down this page!

At the moment the following services are available:

### Twitter Cam

The _Twitter Cam_ can be configured to automatically tweet pictures (together with a text) to a Twitter account via the Twitter API. It is possible to configure Tweets at different times of the day that each have an individual text with them.

The configuration object for Twitter Cam looks like this:

```json
{
  "threaded_daily_tweets": true,
  "secrets": {
    "api_key": "<twitter api key>",
    "api_key_secret": "<twitter api secret>",
    "access_token": "<twitter access token>",
    "access_token_secret": "<twitter access token secret>"
  },
  "timeout": 10
}
```

| key | type | value | description |
| - | - | - | - |
| threaded_daily_tweets | Boolean | true/false | If true, all following Tweets of the day will posted as a reply to the first tweet of the day. **NOT IMPLEMENTED YET!** |
| secrets | Dict | Twitter API secrets | Secrets can be generated in the Twitter developer console. See the [Twitter documentation](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api) for details. |
| timeout | Int | Time in seconds | Defines the timeout for Twitter API calls. Optional, defaults to 5. |

### Timer Cam

The _Timer Cam_ will take pictures in the specified interval and store them on the SD card. If configured, it can also upload them to a FTPS server. A local copy will be kept if requested.

The configuration object for Timer Cam looks like this:

```json
{
  "timer_cam": {
    "active": true,
    "cadence": "1h30s",
    "ftps_upload": {
      "active": true,
      "url": "subdomain.domain.tld",
      "user": "",
      "secret": ""
    }
  }
}
```

| key | type | value | description |
| - | - | - | - |
| active | Boolean | true/false | If true, the service will be active. |
| cadence | String | `NdNhNmNs` formatted time duration | Defines time between two pictures. The first picture is taken immediately after boot. |
| ftps_upload | Object | configuration for FTPS upload sub-feature | Optional. If key is not given, the feature will be inactive. See details below. |

The Timer Cam feature also contains a sub-features which allows upload of the images to FTPS server.

| key | type | value | description |
| - | - | - | - |
| active | Boolean | true/false | If true, the service will be active. |
| url | String | URL (without protocol) | Server to upload the pictures to |
| user | String | FTP username | |
| secret | String | FTP password | |

### Service Runner

The _Service Runner_ is a specific service that has the purpose to run all other the other services according to their schedules. It checks in defined intervals if the services are due to run.

| key | type | value | description |
| - | - | - | - |
| interval | integer | time in seconds | Time in seconds between two runs of the service runner. This time should be considerably lower than the interval of interval-triggered services like Timer Cam with the runtime of the service added on top. Otherwise the next run will start later than the service would be due to run next. |

## Setup

This section describes how you can set up your own _TreeCam_ device.

### Clone the repository

This repository comes with submodules, which need to be initialized when cloning the repository:

```sh
$ git clone git@github.com:frederikheld/treecam.git
$ git submodule init
$ git submodule update
```

### Setup balenaCloud & download image

Follow the [balenaCloud documentation](https://www.balena.io/docs/learn/getting-started/raspberry-pi2/python/) to create a fleet and add a device.

> When downloading the balenaOS image you can already provide your WiFi credentials. In this case you can remove the _wifi-connect_ and _balena-reset_ services from the `docker-compose.yml`. If you do not want to provide the credentials via the cloud (e.g. because you are provisioning a device that will be given to a third party), you can use those services to set and reset your wifi connection via a captive portal and reset button.

### Preapre SD card

It is recommended to use and SD card with 16 GB of storage.

Use the [_Raspberry Pi Imager](https://www.raspberrypi.com/software/) (or similar software) to write the downloaded image to an SD card.

After writing the balenaOS image to the SD card do the following:

> Note: the next steps might not actually be necessary. With the current version of _balenaOS_ this seems to be working out of the box.

In the `resin-boot` partition of the balenaOS SD card edit the file `config.json` and add the following entry to the JSON object:

```json
"os": {
  "udevRules": {
    "99-raspicam": "SUBSYSTEM==\"vchiq\",MODE=\"0666\"\n"
  }
}
```

In the `resin-boot` partition of the balenaOS SD card edit the file `config.txt` and add/edit the following lines:

```
start_x=1
gpu_mem=256 // or 512, if the RasPi has at least 1 GB of RAM
start_file=start_x.elf
fixup_file=fixup_x.dat
```

See for details: https://www.balena.io/docs/learn/develop/hardware/i2c-and-spi/#raspberry-pi-camera-module

You can later overwrite those values for your whole fleet of treecam devices via the fleet variables in balenaCloud. Navigate to "Fleet Variables" and add the following entries:

| Name | Value |
| - | - |
| BALENA_HOST_CONFIG_start_x | 1 |
| BALENA_HOST_CONFIG_gpu_mem | 256 |
| BALENA_HOST_CONFIG_start_file | start_x.elf |
| BALENA_HOST_CONFIG_fixup_file | fixup_x.dat |

### Setup Camera

You need a camera that is compatible to the Rasperry Pi. The easiest way is to use the [official Raspberry Pi Camera Module](https://www.raspberrypi.com/products/camera-module-v2/) but depending on your setup a camera with a real lens might be the better choice.

Be aware that there are 2 types of cameras with lenses:

Some modules are a cobination of camera and lens that are built to go together like [this Adafruit camera](https://www.adafruit.com/product/4561). You can use them out of the box, but they are usually the more expensive choice.

The cheaper choice is to select a lens that can be mounted on top of the official camera module, like the ArduCam lenses. The downside is that this leads to color deviations between the center and the edges of the image which is caused by the different angle in which the light hits the camera sensor with the non-stock lens. This effect is called _lens shading_ and needs to be corrected. See [docs/lens-shading-correction.md](docs/lens-shading-correction.md) for more information.

### Set Timezone

In order to have your services triggered at the right time and to have your timestamps in order, you can set your local timezone for the _camera_ container. This can be done in `docker-compose.yml` in the parent directory. Default is `Europe/Berlin`.

### Configure _camera_ services

_camera_ comes with a set of features that serve a specific purpose. Each feature will either provide or consume an image.

Available services are:

| Name | Purpose | Interface |
| - | - | - |
| [take_picture](src/modules/feature/takepicture.py) | Take a picture with the Raspberry Pi camera | Provides an image |
| [mock_take_picture](src/modules/feature/takepicture.py) | A replacement for _take_picture_ which provides a picture without the need to access Raspberry Pi hardware. Can be used to develop on a non-RasPi computer. | Provides an image |
| [post_on_twitter](src/modules/feature/postontwitter.py) | Posts a picture on Twitter together with a message | Consumes an image |
| [ftps_upload](src/modules/feature/ftpsupload.py) | Uploads a picture to a FTPS server | Consumes an image |

Features are used in combination by services, which each serve a specific use case. Each service uses one feature that provides an image and one one or multiple features that consume images and distribute images. Services are triggered by different events. They are registered with a service runner that periodically checks the services if they are due to run.

Currently there are the following services:

| Name | Purpose | Features | Trigger |
| - | - | - | - |
| [Twitter Cam](src/modules/service/twittercam.py) | Takes picture at defined times of the day an posts them on twitter | take_picture, post_on_twitter | Time of day |
| [Timer Cam](src/modules/service/timercam.py) | Takes a picture and uploads it to an FTPS server | take_picture, ftps_upload | Time interval |

Services can be configured via the `config.json` file. This repository comes with a `config.json_template`, which you can re-name to `config.json`. It comes with a default configuration which you can adapt to your needs.

The first level of the config dict represents the services. There is one service called `global` that can be used to set default values that will be applied to the features in all services but can be overridden per service.

Within the services there are features. Different services can use the same features, but within each service the configuration for the respective feature can be set individually. Service-specific feature configurations will overwrite the global feature configuration.

> Note: the following section is not complete yet. Please refer to the `config.json_template` file to see all configuration options.

### Services

#### Twitter Cam

The Twitter Cam feature will take pictures at given times evey day and post them to Twitter. A local copy will be kept if requested.

### Features

#### Take Picture

The global configuration object looks like this:

```json
{
    "take_picture": {
      "filename_time_format": "%Y-%m-%d_%H-%M-%S"
    }
}
```

| key | type | value | description |
| - | - | - | - |
| filename_time_format | String | datetime template that can be consumed by [strftime()](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior) | Datetime format used in filenames that are stored on internal storage and ftp upload |

#### ftps_upload

// tbd

#### post_on_twitter

// tbd

#### Logging

Logging is done via Python's built-in [`logging`](https://docs.python.org/3/library/logging.html) library. This library has a very complex config, most of which are hidden to the user of _TreeCam_ to simplify the configuration. Some of the config values can be configured feature via `config.json`:

```json
{
  "logging": {
    "level": "INFO",
    "path": "./logfile.txt"
  }
}
```

| key | type | value | description |
| - | - | - | - |
| level | String | DEBUG / INFO / WARNING / ERROR / CRITICAL | see [docs](https://docs.python.org/3/howto/logging.html) |
| logfile | String | path to file where events will be logged | if given, events will be logged to this file, otherwise to `STDOUT` |
