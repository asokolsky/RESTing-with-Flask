from flask import Flask
from logging import Logger
import os
from os.path import abspath, join
import sys
from typing import Optional

# For relative imports to work in Python 3.6
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# main application
app: Optional[Flask] = None
log: Optional[Logger] = None


def create_app(cfgfile: str) -> Flask:
    '''
    Create main app object, while ingesting the settings from the cfgfile
    '''
    global app
    if app is None:
        static_folder = abspath('static')
        app = Flask(
            'farm',
            static_folder=static_folder, static_url_path='',
            instance_path=abspath(join(__file__, '../../conf')),
            instance_relative_config=True)
        print('Serving static content from', static_folder, '...')
        if cfgfile:
            print('Loading config from', cfgfile, '...')
            app.config.from_pyfile(cfgfile)

    from .logger import create_log
    global log
    if log is None:
        log = create_log(app)
    return app


def init_app(app: Flask) -> bool:
    '''
    Get the app ready to serve HTTP requests
    '''
    assert app is not None
    print('Initializing...')
    from . import routes
    from . import dataset

    if not dataset.init_dataset(app.config):
        return False

    return True
