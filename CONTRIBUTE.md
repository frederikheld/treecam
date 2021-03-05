# Contribute

This tutorial focuses on the camera service in `src/camera`.

## Install

Make sure you have Python 3 installed (this code is tested with 3.8.5).

Make sure that `virtualenv` is installed as well.

Navigate to `src/camera` and create a virtual environment that uses Python 3.8:

```sh
$ virtualenv --python /usr/bin/python3.8 camera-env
```

Activate the virtual environment:

```sh
$ source camera-env/bin/activate
```

Install dev packages:

```sh
$ pip install -r requirements-dev.txt
```

## Run tests

Make sure the virtualenv is activated (see above). Run tests with `python -m pytest`.

It is important to not run `pytest` directly as this will result in `ModuleNotFoundError`'s.

## About Design

We have `classes` for different purposes.

### `data` classes

`data` classes are used as data types that store some class of data with the necessary methods to handle it.

`data` classes should not use other `data` classes (no aggregation)!

### `feature` classes

`feature` classes represent a specific feature and hold all data and methods that are related to this feature.


They can make use of `data` classes (aggregation).

A `feature` classes create and/or consume `data` classes.

`feature` classes should not use other `feature` classes (no aggregation)!

### `service` classes

`service` classes represent a service that serves a specifc use case. They are registered with an instance of the `runner` class which acts as an scheduler.

All `service` classes have to inherit from `abstractService` to have the necessary interfaces to interact with the `ServiceRunner`.

`service` classes use `feature` classes to compose their functionality and hold the business logic that brings those features together.
