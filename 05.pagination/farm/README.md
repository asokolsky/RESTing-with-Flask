# Pagination and Queries

As our dataset (farm) grows, we begin to have practical concerns about
efficiency of interaction with it. For example, If we have thousands of
elements in the collection animals, retrieving all of them in one transaction
may be time consuming.  This is undesirable for both the server (too much time
spent on one activity possibly at the expense of the others) and the client
(may leave GUI unresponsive).

_Pagination_ will allow us to page through elements of a long collection without
storing anything on the server.

_Queries_ will allow us to narrow down the set of elements of the collection we
are interested in.

There is definitely more than one way to accomplish either.  

## Pagination

Pagination can be done, for example, either

* through the use of the HTTP headers,
* or through the use of data envelopes.

Both approaches are used in the existing REST APIs.  I prefer the former as it
keeps row data as meta information in the headers.  I find such approach more
elegant.

## Queries

We offer a simple query language which is expressed in terms of URI arguments
alone.  As a result it is intuitive and easy to use.  On a down side it is
pretty limited to very basic queries.

## Server


## Client


## Playing with the Farm


## Testing Farm

