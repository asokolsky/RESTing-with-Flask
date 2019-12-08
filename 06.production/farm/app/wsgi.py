#
# Entry point for the WSGI server
#
from os import getenv
from . import app, app_configure, app_initialize

# print('wsgi.py', __name__)
if __name__ == 'app.wsgi':
    print('wsgi initializing farm app...')
    app_configure(getenv('FLASK_CONFIG'))
    app_initialize()
    # do NOT call run!
