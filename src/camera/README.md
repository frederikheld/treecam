# Camera service

## Preapre SD card

After writing the balenaOS image to the SD card do the following.

> Note: the next steps don't seem to be actually necessary. With the current version of balenaOS this seems to be working out of the box.

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
gpu_mem_512=256
```

You can later overwrite those values for your whole fleet of treecam devices via the fleet variables in balenaCloud. Navigate to "Fleet Variables" and add the following entries:

| Name | Value |
| - | - |
| BALENA_HOST_CONFIG_start_x | 1 |
| BALENA_HOST_CONFIG_gpu_mem_512 | 256 |

If you plan to use devices other than the Raspberry Pi Zero W, you can also add the following variables:

| Name | Value |
| - | - |
| BALENA_HOST_CONFIG_gpu_mem_256 | 192 |
| BALENA_HOST_CONFIG_gpu_mem_1024 | 448 |

balenaOS will then decide depending on the amount of RAM available how much to reserve for the GPU.

Use the accroding value an number for `config.txt` on the SD card as well!

## Apply lens correction

This is only relevant if you're using the original RaspiCam with a third-party lens, like the ArduCam modules. In this case the image might have an uneven color balance between the center and the edges of the image. This is called _lens shading_ and can be corrected. See [docs/lens-shading-correction.md](docs/lens-shading-correction.md) for more information.

## Set Timezone

In order to have your services triggered at the right time and to have your timestamps in order, you can set your local timezone for the _camera_ container. This can be done in `docker-compose.yml` in the parent directory. Default is `Europe/Berlin`.

## Configure _camera_ services

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

The configuration object for Twitter Cam looks like this:

```json
{
  "threaded_daily_tweets": true,
  "secrets": {
    "api_key": "?",
    "api_key_secret": "?",
    "access_token": "?",
    "access_token_secret": "?"
  },
  "timeout": 10
}
```

| key | type | value | description |
| - | - | - | - |
| threaded_daily_tweets | Boolean | true/false | If true, all following Tweets of the day will posted as a reply to the first tweet of the day. NOT IMPLEMENTED YET! |
| secrets | Dict | Twitter API secrets | Secrets can be generated in the Twitter developer console. |
| timeout | Int | Time in seconds | Defines the timeout for Twitter API calls. Optional, defaults to 5 |

#### Timer Cam

The Timer Cam feature will take pictures in the specified interval and store them on the SD card. If configured, it can also upload them to a FTPS server. A local copy will be kept if requested.

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

The service runner is a specific service that has the purpose to run all other services. It checks in defined intervals if the services are due to run.

| key | type | value | description |
| - | - | - | - |
| interval | integer | time in seconds | Time in seconds between two runs of the service runner. This time should be considerably lower than the interval of interval-triggered services like Timer Cam with the runtime of the service added on top. Otherwise the next run will start later than the service would be due to run next. |

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
