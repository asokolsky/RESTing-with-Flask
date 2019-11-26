#
# Entry point for the WSGI server
#
from os import getenv
from . import app, init_app

# print('wsgi.py', __name__)
if __name__ == 'app.wsgi':
    print('wsgi initializing farm app...')
    init_app(getenv('FLASK_CONFIG'))
    # do NOT call run!
