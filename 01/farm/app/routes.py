from flask import jsonify
from . import app

#
# Return JSON not only on valid but also for INvalid URLs
#
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(http_status_code=404, text=str(e)), 404

#
# Say hi in JSON
#
@app.route('/')
@app.route('/index')
def index():
    return jsonify(message='Hello, World!')

