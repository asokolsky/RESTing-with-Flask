# REST Server & Client

## Server

In this section we are adding the following functionality:

* farm schema defined using
[schema](https://github.com/keleshev/schema) package.  Install it using
`pip3 install schema`
* dataset class now works with schema
* APIs animal,POST enforce schema validation
* more unit tests added in the app folder - see below on how to run those.

We made minor improvements to the schema package:
* better handling of enums

## Client

CLI farm client now understands 'all', so that you can do:
```bash
farm animal get all
farm animal del all
```

## Playing with the Farm

Let's start with the low level APIs that used to work for us in the past:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/03/farm$ ./farm -v post /api/v1/animal '{"name":"fluff"}'
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
HTTP POST http://127.0.0.1:44444/api/v1/animal {'name': 'fluff', 'id': 'e738e53e-5354-4b80-88bb-7357c394ac88'}
20191026.160610.267 [10] [140208474548032] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191026.160610.270 [10] [140208474548032] connectionpool.py:396 http://127.0.0.1:44444 "POST /api/v1/animal HTTP/1.1" 409 85
HTTP POST => 409 , {'http_status_code': 409, 'text': "Request data error: Missing keys: 'sex', 'species'"}
got back: {
    "http_status_code": 409,
    "text": "Request data error: Missing keys: 'sex', 'species'"
}
```

We are getting data validation error along with explanation of what is
expected.  Let's supply the requested data:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/03/farm$ ./farm -v post /api/v1/animal '{"name":"fluff", "sex":"female", "species":"chicken"}'
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
HTTP POST http://127.0.0.1:44444/api/v1/animal {'name': 'fluff', 'sex': 'female', 'species': 'chicken', 'id': 'c63226fb-1ae1-4d65-8c5c-c991dea4ae91'}
20191026.160819.216 [10] [139883014424384] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191026.160819.218 [10] [139883014424384] connectionpool.py:396 http://127.0.0.1:44444 "POST /api/v1/animal HTTP/1.1" 201 108
HTTP POST => 201 , {'_href': '/api/v1/animal/c63226fb-1ae1-4d65-8c5c-c991dea4ae91', 'id': 'c63226fb-1ae1-4d65-8c5c-c991dea4ae91'}
got back: {
    "_href": "/api/v1/animal/c63226fb-1ae1-4d65-8c5c-c991dea4ae91",
    "id": "c63226fb-1ae1-4d65-8c5c-c991dea4ae91"
}
alex@latitude:~/Projects/RESTing-with-Flask/03/farm$ ./farm get /api/v1/animal
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
20191026.160939.899 [10] [139829478987584] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191026.160939.901 [10] [139829478987584] connectionpool.py:396 http://127.0.0.1:44444 "GET /api/v1/animal HTTP/1.1" 200 110
got back: [
    {
        "_href": "/api/v1/animal/c63226fb-1ae1-4d65-8c5c-c991dea4ae91",
        "id": "c63226fb-1ae1-4d65-8c5c-c991dea4ae91"
    }
]
```

Now to high level farm client functions:


```bash
alex@latitude:~/Projects/RESTing-with-Flask/03/farm$ ./farm animal get c63226fb-1ae1-4d65-8c5c-c991dea4ae91
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
20191026.161210.562 [10] [140065103394624] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191026.161210.564 [10] [140065103394624] connectionpool.py:396 http://127.0.0.1:44444 "GET /api/v1/animal/c63226fb-1ae1-4d65-8c5c-c991dea4ae91 HTTP/1.1" 200 96
got back: {
    "id": "c63226fb-1ae1-4d65-8c5c-c991dea4ae91",
    "name": "fluff",
    "sex": "female",
    "species": "chicken"
}
```

Check out data validation with higher level API:

```bash

alex@latitude:~/Projects/RESTing-with-Flask/03/farm$ ./farm animal new '{"species":"chicken"}' -n 10
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
20191026.161509.218 [10] [140563344652096] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191026.161509.220 [10] [140563344652096] connectionpool.py:396 http://127.0.0.1:44444 "POST /api/v1/animal HTTP/1.1" 409 73
got back: {
    "http_status_code": 409,
    "text": "Request data error: Missing key: 'sex'"
}
alex@latitude:~/Projects/RESTing-with-Flask/03/farm$ ./farm animal new '{"species":"chicken", "sex":"female"}' -n 10
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
20191026.161601.387 [10] [139732719073088] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191026.161601.390 [10] [139732719073088] connectionpool.py:396 http://127.0.0.1:44444 "POST /api/v1/animal HTTP/1.1" 201 108
got back: {
    "_href": "/api/v1/animal/1c02b74d-7ecf-4c9a-8a75-4ae72f07a2aa",
    "id": "1c02b74d-7ecf-4c9a-8a75-4ae72f07a2aa"
}
20191026.161601.392 [10] [139732719073088] connectionpool.py:243 Resetting dropped connection: 127.0.0.1
20191026.161601.394 [10] [139732719073088] connectionpool.py:396 http://127.0.0.1:44444 "POST /api/v1/animal HTTP/1.1" 201 108
got back: {
    "_href": "/api/v1/animal/902b474b-6d7f-44dc-8e39-e21483a70d69",
    "id": "902b474b-6d7f-44dc-8e39-e21483a70d69"
}
...
alex@latitude:~/Projects/RESTing-with-Flask/03/farm$ ./farm animal del 4a070f6e-9fc6-493a-acc3-6f8b9a13fba4
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
20191026.161909.946 [10] [140600444168000] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191026.161909.948 [10] [140600444168000] connectionpool.py:396 http://127.0.0.1:44444 "DELETE /api/v1/animal/4a070f6e-9fc6-493a-acc3-6f8b9a13fba4 HTTP/1.1" 200 3
got back: {}
```

Now let's try wildcard argument we introduced in this section:

```bash

alex@latitude:~/Projects/RESTing-with-Flask/03/farm$ ./farm animal del all
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
20191026.162917.879 [10] [140337524324160] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191026.162917.881 [10] [140337524324160] connectionpool.py:396 http://127.0.0.1:44444 "GET /api/v1/animal HTTP/1.1" 200 1082
got back: [
    {
        "_href": "/api/v1/animal/c63226fb-1ae1-4d65-8c5c-c991dea4ae91",
        "id": "c63226fb-1ae1-4d65-8c5c-c991dea4ae91"
    },
    {
        "_href": "/api/v1/animal/1c02b74d-7ecf-4c9a-8a75-4ae72f07a2aa",
        "id": "1c02b74d-7ecf-4c9a-8a75-4ae72f07a2aa"
    },
    {
        "_href": "/api/v1/animal/902b474b-6d7f-44dc-8e39-e21483a70d69",
        "id": "902b474b-6d7f-44dc-8e39-e21483a70d69"
    },
    {
        "_href": "/api/v1/animal/c5d05459-055b-4431-bb08-f5152d844934",
        "id": "c5d05459-055b-4431-bb08-f5152d844934"
    },
    {
        "_href": "/api/v1/animal/b4fb5630-e3a6-46f9-b45f-5e333c51c64b",
        "id": "b4fb5630-e3a6-46f9-b45f-5e333c51c64b"
    },
    {
        "_href": "/api/v1/animal/4fae682b-e928-4c54-9aff-010aafc80a29",
        "id": "4fae682b-e928-4c54-9aff-010aafc80a29"
    },
    {
        "_href": "/api/v1/animal/f6f7b6b0-c896-4ebd-a116-4e6929bd033e",
        "id": "f6f7b6b0-c896-4ebd-a116-4e6929bd033e"
    },
    {
        "_href": "/api/v1/animal/e2984038-4c32-4bc2-ac86-0e50ec17e869",
        "id": "e2984038-4c32-4bc2-ac86-0e50ec17e869"
    },
    {
        "_href": "/api/v1/animal/06a32ef8-5b0f-46b2-8f3c-a816da12f34c",
        "id": "06a32ef8-5b0f-46b2-8f3c-a816da12f34c"
    },
    {
        "_href": "/api/v1/animal/46cc979c-1f49-4983-b589-098f447360eb",
        "id": "46cc979c-1f49-4983-b589-098f447360eb"
    }
]
{'_href': '/api/v1/animal/c63226fb-1ae1-4d65-8c5c-c991dea4ae91', 'id': 'c63226fb-1ae1-4d65-8c5c-c991dea4ae91'}
20191026.162917.884 [10] [140337524324160] connectionpool.py:243 Resetting dropped connection: 127.0.0.1
20191026.162917.885 [10] [140337524324160] connectionpool.py:396 http://127.0.0.1:44444 "DELETE /api/v1/animal/c63226fb-1ae1-4d65-8c5c-c991dea4ae91 HTTP/1.1" 200 3
got back: {}
{'_href': '/api/v1/animal/1c02b74d-7ecf-4c9a-8a75-4ae72f07a2aa', 'id': '1c02b74d-7ecf-4c9a-8a75-4ae72f07a2aa'}
20191026.162917.888 [10] [140337524324160] connectionpool.py:243 Resetting dropped connection: 127.0.0.1
20191026.162917.890 [10] [140337524324160] connectionpool.py:396 http://127.0.0.1:44444 "DELETE /api/v1/animal/1c02b74d-7ecf-4c9a-8a75-4ae72f07a2aa HTTP/1.1" 200 3
got back: {}
{'_href': '/api/v1/animal/902b474b-6d7f-44dc-8e39-e21483a70d69', 'id': '902b474b-6d7f-44dc-8e39-e21483a70d69'}
20191026.162917.892 [10] [140337524324160] connectionpool.py:243 Resetting dropped connection: 127.0.0.1
20191026.162917.894 [10] [140337524324160] connectionpool.py:396 http://127.0.0.1:44444 "DELETE /api/v1/animal/902b474b-6d7f-44dc-8e39-e21483a70d69 HTTP/1.1" 200 3
got back: {}
{'_href': '/api/v1/animal/c5d05459-055b-4431-bb08-f5152d844934', 'id': 'c5d05459-055b-4431-bb08-f5152d844934'}
20191026.162917.896 [10] [140337524324160] connectionpool.py:243 Resetting dropped connection: 127.0.0.1
20191026.162917.899 [10] [140337524324160] connectionpool.py:396 http://127.0.0.1:44444 "DELETE /api/v1/animal/c5d05459-055b-4431-bb08-f5152d844934 HTTP/1.1" 200 3
got back: {}
{'_href': '/api/v1/animal/b4fb5630-e3a6-46f9-b45f-5e333c51c64b', 'id': 'b4fb5630-e3a6-46f9-b45f-5e333c51c64b'}
20191026.162917.901 [10] [140337524324160] connectionpool.py:243 Resetting dropped connection: 127.0.0.1
20191026.162917.904 [10] [140337524324160] connectionpool.py:396 http://127.0.0.1:44444 "DELETE /api/v1/animal/b4fb5630-e3a6-46f9-b45f-5e333c51c64b HTTP/1.1" 200 3
got back: {}
{'_href': '/api/v1/animal/4fae682b-e928-4c54-9aff-010aafc80a29', 'id': '4fae682b-e928-4c54-9aff-010aafc80a29'}
20191026.162917.905 [10] [140337524324160] connectionpool.py:243 Resetting dropped connection: 127.0.0.1
20191026.162917.907 [10] [140337524324160] connectionpool.py:396 http://127.0.0.1:44444 "DELETE /api/v1/animal/4fae682b-e928-4c54-9aff-010aafc80a29 HTTP/1.1" 200 3
got back: {}
{'_href': '/api/v1/animal/f6f7b6b0-c896-4ebd-a116-4e6929bd033e', 'id': 'f6f7b6b0-c896-4ebd-a116-4e6929bd033e'}
20191026.162917.909 [10] [140337524324160] connectionpool.py:243 Resetting dropped connection: 127.0.0.1
20191026.162917.912 [10] [140337524324160] connectionpool.py:396 http://127.0.0.1:44444 "DELETE /api/v1/animal/f6f7b6b0-c896-4ebd-a116-4e6929bd033e HTTP/1.1" 200 3
got back: {}
{'_href': '/api/v1/animal/e2984038-4c32-4bc2-ac86-0e50ec17e869', 'id': 'e2984038-4c32-4bc2-ac86-0e50ec17e869'}
20191026.162917.915 [10] [140337524324160] connectionpool.py:243 Resetting dropped connection: 127.0.0.1
20191026.162917.918 [10] [140337524324160] connectionpool.py:396 http://127.0.0.1:44444 "DELETE /api/v1/animal/e2984038-4c32-4bc2-ac86-0e50ec17e869 HTTP/1.1" 200 3
got back: {}
{'_href': '/api/v1/animal/06a32ef8-5b0f-46b2-8f3c-a816da12f34c', 'id': '06a32ef8-5b0f-46b2-8f3c-a816da12f34c'}
20191026.162917.919 [10] [140337524324160] connectionpool.py:243 Resetting dropped connection: 127.0.0.1
20191026.162917.921 [10] [140337524324160] connectionpool.py:396 http://127.0.0.1:44444 "DELETE /api/v1/animal/06a32ef8-5b0f-46b2-8f3c-a816da12f34c HTTP/1.1" 200 3
got back: {}
{'_href': '/api/v1/animal/46cc979c-1f49-4983-b589-098f447360eb', 'id': '46cc979c-1f49-4983-b589-098f447360eb'}
20191026.162917.922 [10] [140337524324160] connectionpool.py:243 Resetting dropped connection: 127.0.0.1
20191026.162917.925 [10] [140337524324160] connectionpool.py:396 http://127.0.0.1:44444 "DELETE /api/v1/animal/46cc979c-1f49-4983-b589-098f447360eb HTTP/1.1" 200 3
got back: {}
alex@latitude:~/Projects/RESTing-with-Flask/03/farm$ ./farm animal get all
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
20191026.162926.350 [10] [139729107265344] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191026.162926.352 [10] [139729107265344] connectionpool.py:396 http://127.0.0.1:44444 "GET /api/v1/animal HTTP/1.1" 200 3
got back: []
```

## Testing Farm

We added tests in the app folder.  To launch all the tests:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/03/farm/app$ python3 -m unittest
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```

The above will look for all the python files starting with test_ and will run
unit test on those.

Alternatively you can test one module at a time:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/03/farm/app$ python3 -m unittest test_dataset -v
test_dataset (test_dataset.TestDataset) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
alex@latitude:~/Projects/RESTing-with-Flask/03/farm/app$ python3 -m unittest test_farm_schema -v
test_animal_schema (test_farm_schema.TestFarmSchema) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```
