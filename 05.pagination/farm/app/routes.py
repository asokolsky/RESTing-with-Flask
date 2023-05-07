import datetime
from flask import jsonify, request, url_for, make_response, Response
from flask.wrappers import Request
from json import dumps
from typing import Any, Dict, Tuple, Union
from schema import SchemaError

from . import app, log, dataset

assert app is not None
assert log is not None


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
def not_found(e):
    return jsonify(http_status_code=404, text=str(e)), 404


def form_elt(id):
    elt = {
        'id': id,
        '_href': url_for('api_animal', id=id),
    }
    return elt


def get_page_args(request: Request) -> Tuple[int, int]:
    '''
    Retrieve the pagination arguments.
    Returns tuple (page, per_page)
    '''
    # log.debug('request.args: %s', str(request.args))
    page = request.args.get('page', default=1, type=int)
    if page <= 0:
        page = 1
    per_page = request.args.get('per_page', default=10, type=int)
    if per_page < 1:
        per_page = 1
    elif per_page > 1000:
        per_page = 1000
    return page, per_page


#
# Animal Collection APIs
#
@app.route('/api/v1/animal', methods=['GET', 'POST'])
def api_animals() -> Union[Response, Tuple[Any, int]]:

    def make_link_header(total: int, page: int, per_page: int) -> str:
        last_page = total // per_page
        if (total % per_page) > 0:
            last_page += 1

        hdrs = []
        if page > 1:
            url = url_for(
                'api_animals',  _external=True, page=1, per_page=per_page)
            hdrs.append('<'+url+'>; rel="first"')
            url = url_for(
                'api_animals',  _external=True, page=page-1, per_page=per_page)
            hdrs.append('<'+url+'>; rel="prev"')

        if page < last_page:
            url = url_for(
                'api_animals',  _external=True, page=page+1, per_page=per_page)
            hdrs.append('<'+url+'>; rel="next"')
            url = url_for(
                'api_animals',  _external=True, page=last_page,
                per_page=per_page)
            hdrs.append('<'+url+'>; rel="last"')

        return ', '.join(hdrs)

    assert dataset.theAnimals is not None
    if request.method == 'GET':
        # get all the animals
        # request may have params like ?page=2&per_page=100
        page, per_page = get_page_args(request)
        total, res = dataset.theAnimals.get_page(page, per_page, form_elt)
        resp = make_response(jsonify(res), 200)

        # form headers
        resp.headers['X-Total-Count'] = total
        resp.headers['Link'] = make_link_header(total, page, per_page)
        return resp

    assert request.method == 'POST'
    # create a new animal from the POSTed data
    rd = request.get_json(force=True, silent=True)
    assert log is not None
    log.info('/api/v1/animal POST %s', str(rd))
    # print('/api/v1/animal POST', str(rd), file=sys.stderr)
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
def api_animal(id):
    dat = dataset.theAnimals.get(id)
    if dat is None:
        return not_found('No such animal: ' + id)

    if request.method == 'GET':
        # get the animal
        return jsonify(dat)

    if request.method == 'DELETE':
        dat = dataset.theAnimals.pop(id)
        # assert dat is not None
        res = {}
        return jsonify(res)

    rd = request.get_json(force=True, silent=True)
    log.info('/api/v1/animal/%s %s %s', id, request.method, str(rd))
    if rd is None:
        return error409('Request must be a JSON')

    if request.method == 'PUT':
        nid = rd.get('id', None)
        if nid is None:
            rd['id'] = id
        elif nid == rd['id']:
            pass
        else:
            return error409('Conflict: URI id vs request id')

        try:
            if dataset.theAnimals.put(id, rd):
                elt = {
                    'id': id,
                    '_href': url_for('api_animal', id=id),
                }
                return jsonify(elt)

        except SchemaError as err:
            return error409('Request data error: ' + str(err))

        return error409('Request data validation failed')

    assert request.method == 'PATCH'
    return error400('Not implemented yet')


@app.route('/api/v1/_conf', methods=['GET'])
def api_conf():
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
