# REST Server & Client

## Server

In this section we are adding the following functionality:

* farm schema defined using
[schema](https://github.com/keleshev/schema) package.  Install it using
`pip3 install schema`
* dataset class now works with schema
* APIs animal,POST enforce schema validation

## Client

TBD

## Playing with the Farm

Test low level APIs:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/02/farm$ ./farm -v post /api/v1/animal '{"name":"fluff"}'
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
HTTP POST http://127.0.0.1:44444/api/v1/animal {'name': 'fluff', 'id': '754e424a-37be-4457-96a1-8f2e0a2ab58c'}
20190926.190251.556 [10] [139791155849024] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20190926.190251.559 [10] [139791155849024] connectionpool.py:396 http://127.0.0.1:44444 "POST /api/v1/animal HTTP/1.1" 200 108
HTTP POST => 200 , {'_href': '/api/v1/animal/754e424a-37be-4457-96a1-8f2e0a2ab58c', 'id': '754e424a-37be-4457-96a1-8f2e0a2ab58c'}
got back: {
    "_href": "/api/v1/animal/754e424a-37be-4457-96a1-8f2e0a2ab58c",
    "id": "754e424a-37be-4457-96a1-8f2e0a2ab58c"
}
alex@latitude:~/Projects/RESTing-with-Flask/02/farm$ ./farm get /api/v1/animal/754e424a-37be-4457-96a1-8f2e0a2ab58c
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
20190926.190459.491 [10] [140564453672768] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20190926.190459.492 [10] [140564453672768] connectionpool.py:396 http://127.0.0.1:44444 "GET /api/v1/animal/754e424a-37be-4457-96a1-8f2e0a2ab58c HTTP/1.1" 200 61
got back: {
    "id": "754e424a-37be-4457-96a1-8f2e0a2ab58c",
    "name": "fluff"
}
```

Now to high level farm client functions:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/02/farm$ ./farm animal get 754e424a-37be-4457-96a1-8f2e0a2ab58c
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
20190926.190617.461 [10] [139689714579264] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20190926.190617.463 [10] [139689714579264] connectionpool.py:396 http://127.0.0.1:44444 "GET /api/v1/animal/754e424a-37be-4457-96a1-8f2e0a2ab58c HTTP/1.1" 200 61
got back: {
    "id": "754e424a-37be-4457-96a1-8f2e0a2ab58c",
    "name": "fluff"
}
alex@latitude:~/Projects/RESTing-with-Flask/02/farm$ ./farm animal new '{"species": "chicken"}' -n 100
...
0190926.190732.499 [10] [139914159785792] connectionpool.py:396 http://127.0.0.1:44444 "POST /api/v1/animal HTTP/1.1" 200 108
got back: {
    "_href": "/api/v1/animal/c15dafc0-73e9-4687-8c99-e6912e0ff360",
    "id": "c15dafc0-73e9-4687-8c99-e6912e0ff360"
}
20190926.190732.501 [10] [139914159785792] connectionpool.py:243 Resetting dropped connection: 127.0.0.1
20190926.190732.506 [10] [139914159785792] connectionpool.py:396 http://127.0.0.1:44444 "POST /api/v1/animal HTTP/1.1" 200 108
got back: {
    "_href": "/api/v1/animal/b0c1201a-4d14-4384-beec-a380f64f83e7",
    "id": "b0c1201a-4d14-4384-beec-a380f64f83e7"
}
alex@latitude:~/Projects/RESTing-with-Flask/02/farm$ ./farm animal del b0c1201a-4d14-4384-beec-a380f64f83e7
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
20190926.191011.586 [10] [140403174364992] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20190926.191011.588 [10] [140403174364992] connectionpool.py:396 http://127.0.0.1:44444 "DELETE /api/v1/animal/b0c1201a-4d14-4384-beec-a380f64f83e7 HTTP/1.1" 200 3
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
