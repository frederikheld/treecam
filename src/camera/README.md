# Camera service

## Preapre SD card

After writing the balenaOS image to the SD card do the following.

> Note: the next steps don't need to be actually necessary.

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

## Configuration

_TreeCam_ comes with different services that each can use different features. The configuration for all of those can be done via `config.json`.

Please rename `config.json_template` to `config.json` and fill in the values according to the detailled description below.

The first level of the config dict represents the services. There is one service called `global` that can be used to set default values that will apply to all features.

Within the services there are features. Different services can use the same features, but within each service the configuration for the respective feature can be set individually. Service-specific feature configurations will overwrite the global feature configuration.

The global configuration object looks like this:

```json
{
    "global": {
      "filename_time_format": "%Y-%m-%d_%H-%M-%S"
    }
}
```

| key | type | value | description |
| - | - | - | - |
| filename_time_format | String | datetime template that can be consumed by [strftime()](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior) | Datetime format used in filenames that are stored on internal storage and ftp upload |

For the feature configurations please see the following sections.

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
| threaded_daily_tweets | Boolean | true/false | If true, all following Tweets of the day will posted as a reply to the first tweet of the day |
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


### Features

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

#### take_picture

// tbd

#### ftps_upload

// tbd

#### post_on_twitter

// tbd
