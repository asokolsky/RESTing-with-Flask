# Farm REST API

## Collections

We start with Farm APIs operating on the following collections of objects:

* animal

Animal has:

* unique identity (id), 
and then some attributes, e.g.:
* name
* sex
* dob
* weight

### Collection Naming: Singular or Plural?

I am sticking with singular.  This is a very much personal preference.
I find a reference to a particular animal 

 /api/v1/animal/fluffy

more readable than

 /api/v1/animals/fluffy

## Animal Collection APIs

All APIs URIs start with '/api/v1' to support versioning.

### /api/v1/animal, GET

Retrieve the list of all the animals.

### /api/v1/animal, POST

Create a new animal record.

### /api/v1/animal/<id>, GET

Retrieve an animal by id.

### /api/v1/animal/<id>, DELETE

Remove the record of a particular animal.

### /api/v1/animal/<id>, PUT

Modify a particular animal record.

### /api/v1/animal/<id>, PATCH

Modify the particular animal record.
