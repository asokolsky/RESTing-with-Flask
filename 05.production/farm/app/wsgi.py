#
# Entry point for the WSGI server
#

from . import app as application
from . import create_app, init_app

if __name__ == 'app.wsgi':
    import os
    global application
    if application is None:
        application = create_app( os.getenv('FLASK_CONFIG') )
    print('wsgi initializing farm app...')
    init_app(application)
    application.run()
