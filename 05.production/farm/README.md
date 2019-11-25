# Going Production

We are adding the following to make the application ready for production
deployment:

* add new endpoints for application version information
* add integration with Prometheus
* add support for deployment with NGINX and uWSGI

## Adding Version Information

The following new endpoints expose application version and configuration
information:

* /api/v1/_about, GET
* /api/v1/_config, GET

To display version in CLI use:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/05.production/farm$ ./farm --version
2019.11.23
```

You can also retrieve it from a running server:

```bash
alex@latitude:~/Projects/RESTing-with-Flask/05.production/farm$ ./farm get /api/v1/_about
Loading config from farm.cfg ...
Logging level set to 10 DEBUG
20191123.174554.486 [10] [140250226689856] connectionpool.py:208 Starting new HTTP connection (1): 127.0.0.1
20191123.174554.488 [10] [140250226689856] connectionpool.py:396 http://127.0.0.1:44444 "GET /api/v1/_about HTTP/1.1" 200 39
got back: {
    "name": "farm",
    "version": "2019.11.23"
}
```

## Prometheus

### Collecting and Exposing Metrics

Prometheus support is implemented in app/metrics.py.  We introduce

* Prometheus counter fro endpoint use;
* Prometheus histogram for latency of each endpoint;
* metric info to supply our application name and version to Prometheus.

During application initialization (see init_app in app/__init__.py))
setup_metrics is called which in turn installs two hooks to be called before
and after every flask request processing.  This allows us to count and time the
processed requests.

We expose the accumulated information to Prometheus for scraping via an
endpoint /api/v1/metrics, GET - see app/routes.py

### Accessing the Metrics

You can and should setup prometheus and grafana (both are readily available
with any mature Linux distribution) and create a dashboard to display farm
data.  Or you could just use a shortcut and point browser to

 http://localhost:44444/api/v1/metrics

The information is presented in a readable and digestible format.

## Production Architecture: NGINX and uWSGI

For development we use a development HTTP server built into FLASK.  This does
not scale for production.  I understand HTTP header processing is taxing and
there are no provisions to start extra instances of the service if the load
increases.

There are multiple options for running FLASK in production.  Here is my
favorite:

* Use [NGINX](https://www.nginx.com) as a front end and to serve static
content.  NGINX is highly efficient at this.
* NGINX natively supports binary [uwsgi
protocol](https://uwsgi-docs.readthedocs.io/en/latest/Protocol.html) to
communicate with FLASK app hosted, e.g. by
[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

The above ensures that:

* heavy lifting in static content serving and HTTP processing is done in native
code by NGINX
* communication with FLASK app is done efficiently using a binary protocol
* FLASK no longer responsible for HTTP header processing
* multiple instances of FLASK app can be used.

The latter also presents a challenge e.g. for collecting prometheus data, but
let's make one step at a time.

## Installing Prometheus, NGINX, uWSGI

All these are readily available from your OS vendor.  I used:

```bash
sudo apt-get install prometheus nginx uwsgi
```

## Putting it all Together

The following pieces glue NGINX, uWSGI and FLASK farm app together:

* conf/nginx_uwsgi.conf is NGINX configuration file. It instructs NGINX to:
    * present itself to outside world at port 44444;
    * serve static content from folder static;
    * route traffic to URIs starting with '/api' to unix socket
    /var/tmp/farm.socket
    
* conf/farm_uwsgi.cfg is our farm configuration file to be used in production.
Note it has interface/port definition absent.
* directory logs will hold server log and pid files
* shell scripts farm_start.sh and farm_stop.sh designed to:
    * start /stop the production server
    * create log and pid files in folder logs
    * backup logs upon start/stop
