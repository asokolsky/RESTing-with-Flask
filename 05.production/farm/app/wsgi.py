#
# Entry point for the WSGI server
#

if __name__ == 'app.wsgi':
    from . import app, init_app
    print('wsgi initializing farm app...')
    init_app(app)
