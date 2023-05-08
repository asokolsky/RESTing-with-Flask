
from flask import request, Response
import time
from prometheus_client import Counter, Histogram, Info

METRICS_INFO = Info('app_version', 'Farm Server Version')
#
#
#
REQUEST_COUNT = Counter(
    'request_count',
    'Request count',
    ['app_name', 'method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'request_latency_sec',
    'Request latency',
    ['app_name', 'endpoint']
)


def on_req_begin() -> None:
    '''
    This will be called before Flask request processing
    '''
    request.start_time = time.time()
    # the processing code can overwrite it, but here is a default:
    request.reported_path = request.path
    return


def on_req_end(response: Response) -> Response:
    '''
    This will be called after Flask request processing
    '''
    resp_time = time.time() - request.start_time
    rpath = request.reported_path
    REQUEST_LATENCY.labels('farm', rpath).observe(resp_time)
    REQUEST_COUNT.labels(
        'farm', request.method, rpath, response.status_code).inc()
    return response


def setup_metrics(app) -> None:
    '''
    Install our hooks into Flask request processing chain
    '''
    from . import __version__

    app.before_request(on_req_begin)
    app.after_request(on_req_end)

    METRICS_INFO.info({
        'app_name': 'farm',
        'app_version': __version__,
    })
    return
