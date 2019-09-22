from flask import jsonify, request, url_for

from . import app
from . import dataset

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
# APIs for animal collection
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
        return jsonify(res)

    assert request.method == 'POST'
    # create a new animal from the POSTed data
    rd = request.get_json(force=True, silent=True, cache=False)
    if rd is None:
        return error409('Request must be a JSON with id')
    id = rd.get('id', None)
    if id is None:
        return error409('Request must be a JSON with id')
    exist = dataset.theAnimals.get(id)
    if exist is not None:
        return error409('Can not POST to an existing entitiy.')
    dataset.theAnimals.put(id, rd)
    elt = { 
        'id' : id,
        '_href' : url_for('api_animal', id=id),
    }
    return jsonify(elt)

@app.route('/api/v1/animal/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def api_animal():
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
