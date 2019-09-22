from flask import jsonify, request, url_for

from . import app
from . import dataset

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


    return jsonify(message='Hello, World!')

@app.route('/api/v1/animal/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def api_animal():
    return jsonify(message='Hello, World!')
