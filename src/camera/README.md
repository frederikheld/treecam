# Camera service

## Preapre SD card

After writing the balenaOS image to the SD card do the following.

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
