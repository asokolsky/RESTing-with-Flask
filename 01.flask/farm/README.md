# Simple Farm - Design and Implementation

## Farm Configuration

Folder conf contains configuration files.  Default configuration file name is
farm.cfg.  This file is read by both farm server and client - after all both
need to know where the server is located.

## Server

We begin with a 'Hello World' server implemented in python3 using
(bare) Flask.

To learn more about building flask applications check out:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

### Starting the Server

Start with this:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/01/farm$ ./farm -h
usage: farm [-h] [-c CONFIG] [-v] {start,get} ...

Farm REST API server.

positional arguments:
  {start,get}           Farm sub-commands
    start               Start Farm REST API development server. Not for
                        production use.
    get                 Issue GET request to the farm server.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Load configuration from CONFIG, defaults to farm.cfg
  -v, --verbose         Tell more about what is going on
alex@latitude:~/Projects/RESTing-with-Flask/01/farm$ ./farm start -h
usage: farm start [-h]

Start Farm REST API development server.

optional arguments:
  -h, --help  show this help message and exit
alex@latitude:~/Projects/RESTing-with-Flask/01/farm$ 
```

To start the server just do this:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/01/farm$ ./farm start
Loading config from farm.cfg ...
Initializing...
 * Serving Flask app "farm" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:44444/ (Press CTRL+C to quit)
 * Restarting with stat
Loading config from farm.cfg ...
Initializing...
 * Debugger is active!
 * Debugger PIN: 335-616-217
```

You can now point your web browser to http://127.0.0.1:44444/ and see the results!

Important things to note:

* the server console produces output when you access the above URL in the
browser.
* the server response to the client (e.g. browser) is in JSON, not HTML.  JSON
is preferred when the results are to be consumed by computer and not human.
* JSON is produced for both valid URLs, e.g. http://127.0.0.1:44444/index and
URLs pointing to non-existing documents: http://127.0.0.1:44444/no/such/thing

We will cover production server deployment later.

### Stopping the Server

Just press Ctrl+C

## Client

Off course you can just use your browser. Point it to the interface and port
specified in the configuration file - defaults to http://127.0.0.1:44444

Alternatively you can use python farm client implemented in:

* launcher farm and
* restc.py

### Using Farm Client

The same farm launcher is used to run a client:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/01$ ./farm/farm -v get index
Loading config from farm.cfg ...
HTTP GET http://127.0.0.1:44444/index ...
HTTP GET http://127.0.0.1:44444/index => 200 , {'message': 'Hello, World!'}
got back: {
    "message": "Hello, World!"
}
```

## Note on Python

Python, being an interpreter, may be late in reporting problems.  Now and then
I run pyflakes:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/01.flask/farm$ pyflakes farm
farm:32: redefinition of unused 'app' from line 29
farm:52: redefinition of unused 'app' from line 49

```

## Note on Flask Process(es)

You can run Flask app threaded or with multiple processes.

