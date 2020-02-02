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

Pagination can be incorporated into Farm API either

* through the use of the HTTP headers, e.g. as in [GitHub
API](https://developer.github.com/v3/#pagination);
* or through the use of data envelopes.

Both approaches are used in the existing REST APIs.  I prefer the former as it
keeps row data as meta information in the headers.  I find such approach [more
elegant](https://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api#pagination.
Our implementation of pagination follows [GitHub
API](https://developer.github.com/v3/guides/traversing-with-pagination/).
The alternative header-based approach to pagination [relies on
Range header](http://otac0n.com/blog/2012/11/21/range-header-i-choose-you.html). 

## Queries

We offer a simple query language which is expressed in terms of URI arguments
alone.  As a result it is intuitive and easy to use.  On a down side it is
pretty limited to very basic queries.

## Server

All the work on support for pagination and queries is done on the server side -
see routes.py

## Client

CLI client improved to:

* support pagination via options --page and --per-page
* include response headers in the printout via options -i/--include, similar to
those in curl.

## Playing with the Farm

```bash
alex@latitude:~/Projects/RESTing-with-Flask/05.pagination/farm$ ./farm -v -i get --page=3 --per-page=5 /api/v1/animal
alex@latitude:~/Projects/RESTing-with-Flask/05.pagination/farm$ ./farm -v -i animal get --page=2 --per-page=3 all
```

Observe:

* response is limited to the number of collection elements as specified in
per-page;
* you can paginate by providing different values for --page;
* header X-Total-Count specifies the total number of elements in the
collection;
* header Link offers URLs for the client to build a paginating GUI.

## Testing Farm
