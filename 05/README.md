# Extending Animal Farm APIs

## New Collections and APIs

At this stage we add new collections:

* herd
* project

Herd is a set of animals, which has its own unique identity (id or name) and
its own set of attributes (e.g. location).

Project is a set of animals, which has its own unique identity (id or name) and
its own set of attributes (e.g. note).

### Herd APIs

#### /api/v1/herd, GET

#### /api/v1/herd, POST

#### /api/v1/herd/<id>, GET

#### /api/v1/herd/<id>, DELETE

#### /api/v1/herd/<id>, PUT

#### /api/v1/herd/<id>, PATCH


## Implementation

See folder farm for the farm API server.

### Running Tests
