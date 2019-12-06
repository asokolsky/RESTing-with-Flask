from datetime import timedelta
from flask import jsonify, request, url_for, make_response
from json import dumps

from . import app, log
from . import dataset

#
# Convenience functions to return an errors
#
def error409(msg):
    return jsonify(http_status_code=409, text=msg), 409

def error400(msg):
    return jsonify(http_status_code=400, text=msg), 400
#
# Return JSON not only on valid but also for INvalid URLs
#
@app.errorhandler(404)
def not_found(e):
    return jsonify(http_status_code=404, text=str(e)), 404

#
# Animal Collection APIs 
#
@app.route('/api/v1/animal', methods=['GET', 'POST'])
def api_animals():
    if request.method == 'GET':
        # get all the animals
        res = []
        for id in dataset.theAnimals.data.keys():
            elt = { 
                'id' : id,
                '_href' : url_for('api_animal', id=id),
            }
            res.append(elt)
        resp = make_response( jsonify(res), 200 )
        resp.headers['X-Total-Count'] = len(res)
        return resp

    assert request.method == 'POST'
    # create a new animal from the POSTed data
    rd = request.get_json(force=True, silent=True) # , cache=False
    log.info('/api/v1/animal POST %s', str(rd))
    if rd is None:
        return error409('Request must be a JSON')

    log.debug('/api/v1/animal POST %s', dumps(rd, indent=4))
    id = rd.get('id', None)
    if id is None:
        return error409('Request must be a JSON with id')
    exist = dataset.theAnimals.get(id)
    if exist is not None:
        return error409('Can not POST to an existing entity.')
    dataset.theAnimals.put(id, rd)
    elt = { 
        'id' : id,
        '_href' : url_for('api_animal', id=id),
    }
    resp = make_response( jsonify(elt), 201 )
    resp.headers['Location'] = url_for('api_animal', id=id, _external=True)
    return resp
    
@app.route('/api/v1/animal/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def api_animal(id):
    dat = dataset.theAnimals.get(id)
    if dat is None:
        return not_found( 'No such animal: ' + id )

    if request.method == 'GET':
        # get the animal
        return jsonify(dat)

    if request.method == 'DELETE':
        dat = dataset.theAnimals.pop(id)
        assert dat is not None
        res = {}
        return jsonify(res)

    if request.method == 'PUT':
        return error400('Not implemented yet')

    assert request.method == 'PATCH'
    return error400('Not implemented yet')

@app.route('/api/v1/_conf', methods=['GET'])
def api_conf():
    res = {} 
    for k,v in app.config.items():
        if(k == 'SECRET_KEY'):
            # keep the secret secret
            continue
        log.debug("%s:%s", k, v)
        if(isinstance(v, timedelta)):
            # this type crashes jsonify
            v = str(v)
        res[ k ] = v
    return jsonify(res)
