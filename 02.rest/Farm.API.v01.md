# Farm REST API

Operates on content type application/json only.

## Collections

We start with Farm APIs operating on the following collections of objects:

* animal

Animal has:

* unique identity (id)

and then some attributes, e.g.:

* name
* sex
* dob
* weight

For now we allow for complete flexibility and do NOT insist on the client
providing any attributes but ID.

### Collection Naming: Singular or Plural?

I am sticking with singular.  This is a very much personal preference.
I find the following reference to a particular animal

 /api/v1/animal/fluffy

more readable than

 /api/v1/animals/fluffy

This point of view is not shared by the majority of the REST API designers.

## Animal Collection APIs

All APIs URIs start with '/api/v1' to support versioning.

### /api/v1/animal, GET

Retrieve the list of all the animals.

HTTP Response Status Code:

* 200 if OK

Note: HTTP response header X-Total-Count carries information on the total count
of the elements returned. Consult [this
discussion](https://stackoverflow.com/questions/3715981/what-s-the-best-restful-method-to-return-total-number-of-items-in-an-object)
for pros and cons of using HTTP headers vs envelope information.

### /api/v1/animal, POST

Create a new animal record.  ID is mandatory

HTTP Response Status Code:

* 201 if the record is created;
* 409 if the posted data validation fails, e.g. the data does not contain ID or
the one is already used.

Note: HTTP response header Location provides URL for accessing the newly
created element of the collection.

### /api/v1/animal/<id>, GET

Retrieve an animal by id.

HTTP Response Status Code:

* 200 if request succeeds.
* 404 if the animal with such an ID does not exist.

### /api/v1/animal/<id>, DELETE

Remove the record of a particular animal.

HTTP Response Status Code:

* 200 if request succeeds.
* 404 if the animal with such an ID does not exist.

### /api/v1/animal/<id>, PUT

Modify a particular animal record.

TODO: document the argument.

HTTP Response Status Code:

* 200 if request succeeds.
* 404 if the animal with such an ID does not exist.

### /api/v1/animal/<id>, PATCH

Modify the particular animal record.

HTTP Response Status Code:

* 200 if request succeeds.
* 404 if the animal with such an ID does not exist.

TODO: document the argument.
