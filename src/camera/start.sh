#!/bin/sh

export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

export PYTHONPATH="${PYTHONPATH}:/src"

echo "CONTENTS OF ."
ls -la

echo "CONTENTS OF ./src"
ls -la ./src

echo "Starting camera process ..."

python3 ./src/__main__.py

