## Common Client/Server Configuration

Folder conf contains configuration files.  Default configuration file name is
helloworld.cfg.  This file is read by both the server and the client - after
all both need to know where the server is located.

## Server

We begin with a 'Hello World' server implemented in python3 using a (bare)
Flask.

To learn more about building flask applications check out the [Flask Mega
Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

### Starting the Server

Start with this:

cd to this directory:

```
alex@latitude:~/Projects/RESTing-with-Flask/01.flask$ cd helloworld/
alex@latitude:~/Projects/RESTing-with-Flask/01.flask/helloworld$ ls -la
total 32
drwxr-xr-x 5 alex alex 4096 May 24 15:02 .
drwxrwxr-x 4 alex alex 4096 May 24 15:02 ..
drwxr-xr-x 3 alex alex 4096 Nov 17  2019 app
drwxrwxr-x 2 alex alex 4096 May 24 15:03 conf
-rwxrwxr-x 1 alex alex 2913 May 24 15:11 helloworld
drwxr-xr-x 2 alex alex 4096 Nov 23  2019 __pycache__
-rw-r--r-- 1 alex alex 3617 May 24 15:12 README.md
-rw-r--r-- 1 alex alex 1225 Sep 21  2019 restc.py
```
Then run:

```
alex@latitude:~/Projects/RESTing-with-Flask/01.flask/helloworld$ ./helloworld -h
usage: helloworld [-h] [-c CONFIG] [-v] {start,get} ...

HelloWorld REST API server.

positional arguments:
  {start,get}           HelloWorld sub-commands
    start               Start the REST API development server. Not for
                        production use.
    get                 Issue GET request to the REST API server.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Load configuration from CONFIG, defaults to
                        helloworld.cfg
  -v, --verbose         Tell more about what is going on
alex@latitude:~/Projects/RESTing-with-Flask/01.flask/helloworld$ ./helloworld start -h
usage: helloworld start [-h]

Start the REST API development server.

optional arguments:
  -h, --help  show this help message and exit
```

To start the server just do:

```
alex@latitude:~/Projects/RESTing-with-Flask/01.flask/helloworld$ ./helloworld start
Starting service pid 21804
Loading config from helloworld.cfg ...
Initializing...
 * Serving Flask app "helloworld" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:44444/ (Press CTRL+C to quit)
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

Alternatively you can use python helloworld client implemented in:

* launcher helloworld and
* restc.py

### Using HelloWorld Client

The same helloworld launcher is used to run a client:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/01.flask/helloworld$ ./helloworld -v get index
Loading config from helloworld.cfg ...
HTTP GET http://127.0.0.1:44444/index ...
HTTP GET http://127.0.0.1:44444/index => 200 , {'message': 'Hello, World!'}
got back: {
    "message": "Hello, World!"
}
```

## Note on Python

Python, being an interpreter, may be late in reporting problems.
Now and then I run pyflakes:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/01.flask/helloworld$ pyflakes ./helloworld
./helloworld:47:65: invalid syntax
        print( 'Ctrl-C caught in service start, aborting.', file=stderr )
                                                                ^
alex@latitude:~/Projects/RESTing-with-Flask/01.flask/helloworld$ pyflakes *.py
alex@latitude:~/Projects/RESTing-with-Flask/01.flask/helloworld$ pyflakes app/*.py
app/__init__.py:26: '.routes' imported but unused
```

## Note on Flask Process(es)

You can run Flask app threaded or with multiple processes.  For now we are running
it in a default configuration: single process with threading enabled.
