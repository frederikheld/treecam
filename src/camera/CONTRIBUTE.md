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
