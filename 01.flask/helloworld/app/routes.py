from flask import jsonify
from typing import Any, Tuple
from . import app
assert app is not None


#
# Return JSON not only on valid but also for INvalid URLs
#
@app.errorhandler(404)
def page_not_found(e: Any) -> Tuple[str, int]:
    return jsonify(http_status_code=404, text=str(e)), 404


#
# Say hi in JSON
#
@app.route('/')
@app.route('/index')
def index():
    return jsonify(message='Hello, World!')
