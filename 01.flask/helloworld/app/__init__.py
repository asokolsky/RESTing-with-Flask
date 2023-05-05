from os.path import abspath, join
from flask import Flask
from typing import Any

# main application
app = None


def create_app(cfgfile: str) -> Any:
    '''
    Create main app object, while ingesting the settings from the cfgfile
    '''
    global app
    if app is None:
        app = Flask(
            'helloworld',
            instance_path=abspath(join(__file__, '../../conf')),
            instance_relative_config=True)
    if cfgfile:
        print('Loading config from', cfgfile, '...')
        app.config.from_pyfile(cfgfile)

    return app


def init_app(app):
    assert app is not None
    print('Initializing...')
    from . import routes
    return
