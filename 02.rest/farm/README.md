# REST Service & Client

## Farm API Server

Farm API v1 is implemented in the following files:

* app/dataset.py implements in-memory data storage for animals;
* app/routes.py implements REST APIs for animal collection;
* except that methods PUT and PATCH are not implemented yet;
* as before, folder conf contains Farm configuration.  It is consulted by both
the server and the client.

As before, farm server is launched using farm start command.

We added:

* some logging for extra verbosity.
Here is a decent [primer on flask logging](https://www.scalyr.com/blog/getting-started-quickly-with-flask-logging/).
* provisions for serving static content from folder static.

## Client

Module [restc.py](restc.py) has python implementation of HTTP client.  It
relies on a session (as opposed to request object) in order to maintain context
between the calls.  This is important not only for performance reasons (no need
to re-establish TCP connection) but later will make possible client login.

Farm python client now supports HTTP POST.  Along with the previously
implemented GET those two constitute a low level farm actions.  Moreover, farm
python client now adds high level actions for animal collection:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/02.rest/farm$ ./farm -h
usage: farm [-h] [-c CONFIG] [-v] [-i] {start,get,post,animal} ...

Farm REST API server.

positional arguments:
  {start,get,post,animal}
                        Farm sub-commands
    start               Start Farm REST API development server. Not for
                        production use.
    get                 Issue GET request to the farm server.
    post                Issue POST request to the farm server.
    animal              Issue animal commands to the farm server.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Load configuration from CONFIG, defaults to farm.cfg
  -v, --verbose         Tell more about what is going on
  -i, --include         Include protocol headers in the output.

alex@latitude:~/Projects/RESTing-with-Flask/02.rest/farm$ ./farm animal -h
usage: farm animal [-h] [-n NUM] {new,get,del} data [data ...]

Issue animal commands.

positional arguments:
  {new,get,del}      Animal command, determines how data argument is
                     interpreted.
  data               Animal data. Must be JSON for new (ID will be added) or
                     animal ID for the other commands.

optional arguments:
  -h, --help         show this help message and exit
  -n NUM, --num NUM  Repeat command this many times. Defaults to the number of
                     times the data is specified.

```

## Playing with the Farm

Test low level APIs:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/02.rest/farm$ ./farm -v -i post /api/v1/animal '{"name":"fluff"}'
Serving static content from /home/alex/Projects/RESTing-with-Flask/02.rest/farm/static ...
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
HTTP POST http://127.0.0.1:44444/api/v1/animal {'name': 'fluff', 'id': '3f38c3bb-f910-4701-9d40-01ab6a265e84'} ...
20191206.104849.515 [10] [139855935874880] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191206.104849.518 [10] [139855935874880] connectionpool.py:396 http://127.0.0.1:44444 "POST /api/v1/animal HTTP/1.1" 201 108
HTTP POST => 201 , {'_href': '/api/v1/animal/3f38c3bb-f910-4701-9d40-01ab6a265e84', 'id': '3f38c3bb-f910-4701-9d40-01ab6a265e84'}
HTTP Response Headers:
    Content-Type : application/json
    Content-Length : 108
    Location : http://127.0.0.1:44444/api/v1/animal/3f38c3bb-f910-4701-9d40-01ab6a265e84
    Server : Werkzeug/0.15.6 Python/3.6.9
    Date : Fri, 06 Dec 2019 18:48:49 GMT
got back: {
    "_href": "/api/v1/animal/3f38c3bb-f910-4701-9d40-01ab6a265e84",
    "id": "3f38c3bb-f910-4701-9d40-01ab6a265e84"
}
alex@latitude:~/Projects/RESTing-with-Flask/02.rest/farm$ ./farm -vi get /api/v1/animal/3f38c3bb-f910-4701-9d40-01ab6a265e84
Serving static content from /home/alex/Projects/RESTing-with-Flask/02.rest/farm/static ...
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
HTTP GET http://127.0.0.1:44444/api/v1/animal/3f38c3bb-f910-4701-9d40-01ab6a265e84  ...
20191206.105011.503 [10] [140159289902912] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191206.105011.505 [10] [140159289902912] connectionpool.py:396 http://127.0.0.1:44444 "GET /api/v1/animal/3f38c3bb-f910-4701-9d40-01ab6a265e84 HTTP/1.1" 200 61
HTTP GET => 200 , {'id': '3f38c3bb-f910-4701-9d40-01ab6a265e84', 'name': 'fluff'}
HTTP Response Headers:
    Content-Type : application/json
    Content-Length : 61
    Server : Werkzeug/0.15.6 Python/3.6.9
    Date : Fri, 06 Dec 2019 18:50:11 GMT
got back: {
    "id": "3f38c3bb-f910-4701-9d40-01ab6a265e84",
    "name": "fluff"
}
```

Now to high level farm client functions:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/02.rest/farm$ ./farm animal new '{"species": "chicken"}' -n 100
Serving static content from /home/alex/Projects/RESTing-with-Flask/02.rest/farm/static ...
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
20191206.105202.620 [10] [140118676305728] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191206.105202.622 [10] [140118676305728] connectionpool.py:396 http://127.0.0.1:44444 "POST /api/v1/animal HTTP/1.1" 201 108
got back: {
    "_href": "/api/v1/animal/7bf4881c-fdb7-441a-96ed-10eef1e19f71",
    "id": "7bf4881c-fdb7-441a-96ed-10eef1e19f71"
}
20191206.105202.625 [10] [140118676305728] connectionpool.py:243 Resetting dropped connection: 127.0.0.1
20191206.105202.627 [10] [140118676305728] connectionpool.py:396 http://127.0.0.1:44444 "POST /api/v1/animal HTTP/1.1" 201 108
got back: {
    "_href": "/api/v1/animal/e46231db-aec6-4c0e-8d82-4c0b97e2a826",
    "id": "e46231db-aec6-4c0e-8d82-4c0b97e2a826"
}
...
alex@latitude:~/Projects/RESTing-with-Flask/02.rest/farm$ ./farm -vi animal get e46231db-aec6-4c0e-8d82-4c0b97e2a826
Serving static content from /home/alex/Projects/RESTing-with-Flask/02.rest/farm/static ...
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
HTTP GET http://127.0.0.1:44444/api/v1/animal/e46231db-aec6-4c0e-8d82-4c0b97e2a826  ...
20191206.105733.135 [10] [140293511788352] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191206.105733.137 [10] [140293511788352] connectionpool.py:396 http://127.0.0.1:44444 "GET /api/v1/animal/e46231db-aec6-4c0e-8d82-4c0b97e2a826 HTTP/1.1" 200 66
HTTP GET => 200 , {'id': 'e46231db-aec6-4c0e-8d82-4c0b97e2a826', 'species': 'chicken'}
HTTP Response Headers:
    Content-Type : application/json
    Content-Length : 66
    Server : Werkzeug/0.15.6 Python/3.6.9
    Date : Fri, 06 Dec 2019 18:57:33 GMT
got back: {
    "id": "e46231db-aec6-4c0e-8d82-4c0b97e2a826",
    "species": "chicken"
}
alex@latitude:~/Projects/RESTing-with-Flask/02.rest/farm$ ./farm -vi animal del e46231db-aec6-4c0e-8d82-4c0b97e2a826
Serving static content from /home/alex/Projects/RESTing-with-Flask/02.rest/farm/static ...
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
HTTP DELETE http://127.0.0.1:44444/api/v1/animal/e46231db-aec6-4c0e-8d82-4c0b97e2a826  ...
20191206.105758.914 [10] [139812748801856] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191206.105758.916 [10] [139812748801856] connectionpool.py:396 http://127.0.0.1:44444 "DELETE /api/v1/animal/e46231db-aec6-4c0e-8d82-4c0b97e2a826 HTTP/1.1" 200 3
HTTP DELETE => 200 , {}
HTTP Response Headers:
    Content-Type : application/json
    Content-Length : 3
    Server : Werkzeug/0.15.6 Python/3.6.9
    Date : Fri, 06 Dec 2019 18:57:58 GMT
got back: {}
```

## Testing Farm

HTTP client implementation is tested in test_restc.py against an external web
site http://httpbin.org, so your internet connection should be up for this to
work.

test_farm.py relies on a builtin flask test client, so the farm application
does not even have to run for the test to work!

To launch all the tests:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/02/farm$ python3 -m unittest
```

The above will look for all the python files starting with test_ and will run
unit test on those.

Alternatively you can test one module at a time:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/02/farm$ python3 test_restc.py
alex@latitude:~/Projects/RESTing-with-Flask/02/farm$ python3 test_farm.py
```
