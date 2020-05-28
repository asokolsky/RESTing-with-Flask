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

Python comes with a built-in unit test support.  Let us take advantage of it.

HTTP client implementation is tested in test_restc.py against an external web
site http://httpbin.org, so your internet connection should be up for this to
work.

test_farm.py relies on a builtin flask test client, so the farm application
does not even have to run for the test to work!

To launch all the tests:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/02.rest/farm$ python3 -m unittest
Serving static content from /home/alex/Projects/RESTing-with-Flask/02.rest/farm/static ...
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
Initializing...
20200527.214410.709 [20] [139818624431936] routes.py:44 /api/v1/animal POST {'id': '28dc2583-5ca5-4a89-aebc-60d07c0c8fdb', 'weight': 4500}
20200527.214410.710 [10] [139818624431936] routes.py:48 /api/v1/animal POST {
    "id": "28dc2583-5ca5-4a89-aebc-60d07c0c8fdb",
    "weight": 4500
}
20200527.214410.711 [20] [139818624431936] routes.py:44 /api/v1/animal POST {'id': 'd9893f1a-4ac1-4092-88c8-438757fbc518', 'weight': 4500}
20200527.214410.711 [10] [139818624431936] routes.py:48 /api/v1/animal POST {
    "id": "d9893f1a-4ac1-4092-88c8-438757fbc518",
    "weight": 4500
}
20200527.214410.713 [20] [139818624431936] routes.py:44 /api/v1/animal POST {'id': '81b4b17a-c966-4266-8a4c-b1585f24c0aa', 'weight': 4500}
20200527.214410.713 [10] [139818624431936] routes.py:48 /api/v1/animal POST {
    "id": "81b4b17a-c966-4266-8a4c-b1585f24c0aa",
    "weight": 4500
}
20200527.214410.714 [20] [139818624431936] routes.py:44 /api/v1/animal POST {'id': '2baf756d-ba4c-4065-87c5-097b5039a0cb', 'weight': 4500}
20200527.214410.714 [10] [139818624431936] routes.py:48 /api/v1/animal POST {
    "id": "2baf756d-ba4c-4065-87c5-097b5039a0cb",
    "weight": 4500
}
20200527.214410.716 [20] [139818624431936] routes.py:44 /api/v1/animal POST {'id': '83daabbf-c5eb-4b07-aae1-8c55d5fc6077', 'weight': 4500}
20200527.214410.716 [10] [139818624431936] routes.py:48 /api/v1/animal POST {
    "id": "83daabbf-c5eb-4b07-aae1-8c55d5fc6077",
    "weight": 4500
}
.HTTP DELETE http://httpbin.org:80/delete  ...
20200527.214410.724 [10] [139818624431936] connectionpool.py:208 Starting new HTTP connection (1): httpbin.org
20200527.214410.902 [10] [139818624431936] connectionpool.py:396 http://httpbin.org:80 "DELETE /delete HTTP/1.1" 200 401
HTTP DELETE => 200 , {'args': {}, 'data': '', 'files': {}, 'form': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Content-Length': '0', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.18.4', 'X-Amzn-Trace-Id': 'Root=1-5ecf419a-ae037360efa3ac10212f3c24'}, 'json': None, 'origin': '76.103.188.220', 'url': 'http://httpbin.org/delete'}
HTTP Response Headers:
    Date : Thu, 28 May 2020 04:44:10 GMT
    Content-Type : application/json
    Content-Length : 401
    Connection : keep-alive
    Server : gunicorn/19.9.0
    Access-Control-Allow-Origin : *
    Access-Control-Allow-Credentials : true
.HTTP GET http://httpbin.org:80/ip  ...
20200527.214410.908 [10] [139818624431936] connectionpool.py:208 Starting new HTTP connection (1): httpbin.org
20200527.214411.072 [10] [139818624431936] connectionpool.py:396 http://httpbin.org:80 "GET /ip HTTP/1.1" 200 33
HTTP GET => 200 , {'origin': '76.103.188.220'}
HTTP Response Headers:
    Date : Thu, 28 May 2020 04:44:11 GMT
    Content-Type : application/json
    Content-Length : 33
    Connection : keep-alive
    Server : gunicorn/19.9.0
    Access-Control-Allow-Origin : *
    Access-Control-Allow-Credentials : true
HTTP GET http://httpbin.org:80/user-agent  ...
20200527.214411.160 [10] [139818624431936] connectionpool.py:396 http://httpbin.org:80 "GET /user-agent HTTP/1.1" 200 45
HTTP GET => 200 , {'user-agent': 'python-requests/2.18.4'}
HTTP Response Headers:
    Date : Thu, 28 May 2020 04:44:11 GMT
    Content-Type : application/json
    Content-Length : 45
    Connection : keep-alive
    Server : gunicorn/19.9.0
    Access-Control-Allow-Origin : *
    Access-Control-Allow-Credentials : true
HTTP GET http://httpbin.org:80/get  ...
20200527.214411.257 [10] [139818624431936] connectionpool.py:396 http://httpbin.org:80 "GET /get HTTP/1.1" 200 307
HTTP GET => 200 , {'args': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.18.4', 'X-Amzn-Trace-Id': 'Root=1-5ecf419b-b7518e2b15406934caf4ad63'}, 'origin': '76.103.188.220', 'url': 'http://httpbin.org/get'}
HTTP Response Headers:
    Date : Thu, 28 May 2020 04:44:11 GMT
    Content-Type : application/json
    Content-Length : 307
    Connection : keep-alive
    Server : gunicorn/19.9.0
    Access-Control-Allow-Origin : *
    Access-Control-Allow-Credentials : true
.HTTP PATCH http://httpbin.org:80/patch {'a': 'value-of-a', 'b': 1234, 'c': {'d': ['I', 'love', 'REST'], 'e': 'done'}} ...
20200527.214411.262 [10] [139818624431936] connectionpool.py:208 Starting new HTTP connection (1): httpbin.org
20200527.214411.420 [10] [139818624431936] connectionpool.py:396 http://httpbin.org:80 "PATCH /patch HTTP/1.1" 200 685
HTTP PATCH => 200 , {'args': {}, 'data': '{"a": "value-of-a", "b": 1234, "c": {"d": ["I", "love", "REST"], "e": "done"}}', 'files': {}, 'form': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Content-Length': '78', 'Content-Type': 'application/json', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.18.4', 'X-Amzn-Trace-Id': 'Root=1-5ecf419b-f484deda23f9fd1e54a446c6'}, 'json': {'a': 'value-of-a', 'b': 1234, 'c': {'d': ['I', 'love', 'REST'], 'e': 'done'}}, 'origin': '76.103.188.220', 'url': 'http://httpbin.org/patch'}
HTTP Response Headers:
    Date : Thu, 28 May 2020 04:44:11 GMT
    Content-Type : application/json
    Content-Length : 685
    Connection : keep-alive
    Server : gunicorn/19.9.0
    Access-Control-Allow-Origin : *
    Access-Control-Allow-Credentials : true
.HTTP POST http://httpbin.org:80/post {'a': 'value-of-a', 'b': 1234, 'c': {'d': ['I', 'love', 'REST'], 'e': 'done'}} ...
20200527.214411.426 [10] [139818624431936] connectionpool.py:208 Starting new HTTP connection (1): httpbin.org
20200527.214411.586 [10] [139818624431936] connectionpool.py:396 http://httpbin.org:80 "POST /post HTTP/1.1" 200 684
HTTP POST => 200 , {'args': {}, 'data': '{"a": "value-of-a", "b": 1234, "c": {"d": ["I", "love", "REST"], "e": "done"}}', 'files': {}, 'form': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Content-Length': '78', 'Content-Type': 'application/json', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.18.4', 'X-Amzn-Trace-Id': 'Root=1-5ecf419b-66131cd4097988a6ede65c40'}, 'json': {'a': 'value-of-a', 'b': 1234, 'c': {'d': ['I', 'love', 'REST'], 'e': 'done'}}, 'origin': '76.103.188.220', 'url': 'http://httpbin.org/post'}
HTTP Response Headers:
    Date : Thu, 28 May 2020 04:44:11 GMT
    Content-Type : application/json
    Content-Length : 684
    Connection : keep-alive
    Server : gunicorn/19.9.0
    Access-Control-Allow-Origin : *
    Access-Control-Allow-Credentials : true
.HTTP PUT http://httpbin.org:80/put {'a': 'value-of-a', 'b': 1234, 'c': {'d': ['I', 'love', 'REST'], 'e': 'done'}} ...
20200527.214411.592 [10] [139818624431936] connectionpool.py:208 Starting new HTTP connection (1): httpbin.org
20200527.214411.752 [10] [139818624431936] connectionpool.py:396 http://httpbin.org:80 "PUT /put HTTP/1.1" 200 683
HTTP PUT => 200 , {'args': {}, 'data': '{"a": "value-of-a", "b": 1234, "c": {"d": ["I", "love", "REST"], "e": "done"}}', 'files': {}, 'form': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Content-Length': '78', 'Content-Type': 'application/json', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.18.4', 'X-Amzn-Trace-Id': 'Root=1-5ecf419b-1634e8c8e60acaf84984b138'}, 'json': {'a': 'value-of-a', 'b': 1234, 'c': {'d': ['I', 'love', 'REST'], 'e': 'done'}}, 'origin': '76.103.188.220', 'url': 'http://httpbin.org/put'}
HTTP Response Headers:
    Date : Thu, 28 May 2020 04:44:11 GMT
    Content-Type : application/json
    Content-Length : 683
    Connection : keep-alive
    Server : gunicorn/19.9.0
    Access-Control-Allow-Origin : *
    Access-Control-Allow-Credentials : true
.
----------------------------------------------------------------------
Ran 6 tests in 1.056s

OK
alex@latitude:~/Projects/RESTing-with-Flask/02.rest/farm$ 
```

The above command looks for all the python files starting with test_ and runs
unit test on those.

Alternatively you can test one module at a time:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/02.rest/farm$ python3 test_restc.py
alex@latitude:~/Projects/RESTing-with-Flask/02.rest/farm$ python3 test_farm.py
```
