#!/bin/sh

export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

echo "Hello from the Camera service!"

ls -a

python3 take-picture.py

ls -a
