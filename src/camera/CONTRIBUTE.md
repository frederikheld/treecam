# About Design

We have `data` classes and `feature` classes.

## `data` classes

`data` classes are used as data types that store some class of data with the necessary methods to handle it.

`data` classes should not use other `data` classes (no aggregation)!

## `feature` classes

`feature` classes represent a specific feature and hold all data and methods that are related to this feature.

They can make use of `data` classes (aggregation).

Apart from primitive types, `data` objects are also the preferred way to pass values in and out of `feature` classes.

`feature` classes should not use other `feature` classes (no aggregation)!

## `service` classes

`service` classes represent a specific service that can be run at the configured times. The are registered with an instance of the `runner` class which acts as an scheduler.

All `service` classes have to inherit from `abstractService` to have the necessary interfaces to interact with the `runner`.

`service` classes can use `feature` classes to compose their functionality.
