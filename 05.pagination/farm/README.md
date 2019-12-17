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
elegant](https://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api#pagination).

Our implementation of pagination:

* follows [GitHub API](https://developer.github.com/v3/guides/traversing-with-pagination/).
* relies on [URI template](https://tools.ietf.org/html/rfc6570) [Python
library](https://uritemplate.readthedocs.io/en/latest/)

Install uritemplate python library:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/05.pagination$ pip3 install uritemplate
Collecting uritemplate
  Downloading https://files.pythonhosted.org/packages/e5/7d/9d5a640c4f8bf2c8b1afc015e9a9d8de32e13c9016dcc4b0ec03481fb396/uritemplate-3.0.0-py2.py3-none-any.whl
Installing collected packages: uritemplate
Successfully installed uritemplate-3.0.0
```

## Queries

We offer a simple query language which is expressed in terms of URI arguments
alone.  As a result it is intuitive and easy to use.  On a down side it is
pretty limited to very basic queries.

## Server

## Client

## Playing with the Farm

## Testing Farm

