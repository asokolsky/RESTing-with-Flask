# Simple Farm - Design and Implementation

## Server

We are starting with a 'Hello World' server implemented in pythoon3 using (bare) Flask.

To learn more about building flask applications check out:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

### Server Configuration

Folder conf contains configuration files.  Default configration file name is farm.cfg.

### Starting the Server

Start with this: 

```
alex@latitude:~/Projects/RESTing-with-Flask/01$ 
alex@latitude:~/Projects/RESTing-with-Flask/01$ cd farm
alex@latitude:~/Projects/RESTing-with-Flask/01/farm$ ./
app/  conf/ farm  
alex@latitude:~/Projects/RESTing-with-Flask/01/farm$ ./farm -h
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

```
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
* output displayed in the browser is in JSON, not HTML - preferred format when
the results are to be consumed by computer and not humans.
* JSON is produced for both valid URLs, e.g. http://127.0.0.1:44444/index and
URLs pointing to non-existing documents: http://127.0.0.1:44444/no/such/thing

We will cover production server deployment later.

### Stopping the Server

Just press Ctrl+C

### Running the Client

Offcourse you can just use your browser. Point it to the interface and port
specified in the configuration file - defaults to http://127.0.0.1:44444

Alternatively, you can:
```

```

Python REST client is implemented in the following modules:

* launcher farm and
* restc.py

