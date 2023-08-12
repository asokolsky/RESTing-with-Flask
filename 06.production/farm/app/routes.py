import datetime
from flask import jsonify, request, url_for, make_response, Response
from json import dumps
from prometheus_client import generate_latest
from schema import SchemaError
from typing import Any, Dict, Tuple, Union

from . import app, log
from . import dataset


#
# Convenience functions to return an errors
#
def error409(msg: str) -> Tuple[Any, int]:
    return jsonify(http_status_code=409, text=msg), 409


def error400(msg: str) -> Tuple[Any, int]:
    return jsonify(http_status_code=400, text=msg), 400


#
# Return JSON not only on valid but also for INvalid URLs
#
@app.errorhandler(404)
def not_found(e) -> Tuple[Any, int]:
    return jsonify(http_status_code=404, text=str(e)), 404


#
# Animal Collection APIs
#
@app.route('/api/v1/animal', methods=['GET', 'POST'])
def api_animals() -> Union[Response, Tuple[Any, int]]:
    assert dataset.theAnimals is not None
    if request.method == 'GET':
        # get all the animals
        res = []
        for id in dataset.theAnimals.ids():
            elt = {
                'id': id,
                '_href': url_for('api_animal', id=id),
            }
            res.append(elt)
        resp = make_response(jsonify(res), 200)
        resp.headers['X-Total-Count'] = len(res)
        return resp

    assert request.method == 'POST'
    # create a new animal from the POSTed data
    rd = request.get_json(force=True, silent=True)
    log.info('/api/v1/animal POST %s', str(rd))
    if rd is None:
        return error409('Request must be a JSON')

    log.debug('/api/v1/animal POST %s', dumps(rd, indent=4))
    id = rd.get('id', None)
    if id is None:
        return error409('Request must be a JSON with id')
    exists = dataset.theAnimals.get(id)
    if exists is not None:
        return error409('Can not POST to an existing entity.')
    try:
        if dataset.theAnimals.put(id, rd):
            elt = {
                'id': id,
                '_href': url_for('api_animal', id=id),
            }
            resp = make_response(jsonify(elt), 201)
            resp.headers['Location'] = url_for(
                'api_animal', id=id, _external=True)
            return resp

    except SchemaError as err:
        return error409('Request data error: ' + str(err))

    return error409('Request data validation failed')


@app.route('/api/v1/animal/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def api_animal(id: str) -> Union[Response, Tuple[Any, int]]:
    assert dataset.theAnimals is not None
    dat = dataset.theAnimals.get(id)
    if dat is None:
        return not_found('No such animal: ' + id)

    if request.method == 'GET':
        # get the animal
        return jsonify(dat)

    if request.method == 'DELETE':
        dataset.theAnimals.pop(id)
        return jsonify({})

    if request.method == 'PUT':
        return error400('Not implemented yet')

    assert request.method == 'PATCH'
    return error400('Not implemented yet')


@app.route('/api/v1/_about', methods=['GET'])
def api_about() -> Response:
    from . import __version__
    dat = {
        'name': app.name,
        'version': __version__
    }
    return jsonify(dat)


@app.route('/api/v1/_conf', methods=['GET'])
def api_conf() -> Response:
    res = {}
    for k, v in app.config.items():
        if k == 'SECRET_KEY':
            # keep the secret secret
            continue
        log.debug("%s:%s", k, v)
        if isinstance(v, datetime.timedelta):
            # this type crashes jsonify
            v = str(v)
        res[k] = v
    return jsonify(res)


@app.route('/api/v1/metrics', methods=['GET'])
def api_metrics():
    r = make_response(generate_latest(), 200)
    r.mimetype = 'text/plain; version=0.0.4; charset=utf-8'
    return r
