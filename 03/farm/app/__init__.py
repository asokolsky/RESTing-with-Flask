# For relative imports to work in Python 3.6
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import logging
from logging import getLogger, CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
from os.path import abspath, join
from flask import Flask

# main application
app = None
log = None

def create_app( cfgfile ):
    '''
    Create main app object, while ingesting the settings from the cfgfile
    '''
    global app
    global log
    if app is None:
        app = Flask(
            'farm', #__name__,
            static_folder='static',
            static_url_path='',
            instance_path=abspath(join( __file__, '../../conf' )),
            instance_relative_config=True)
        if cfgfile:
            print('Loading config from', cfgfile, '...')
            app.config.from_pyfile(cfgfile)

    if log is None:
        mfmt = "%(asctime)s.%(msecs)03d [%(levelno)s] [%(thread)d] %(filename)s:%(lineno)s %(message)s"
        logging.basicConfig(format=mfmt, datefmt="%Y%m%d.%H%M%S")
        log = getLogger()
        level = app.config.get('LOGGING_LEVEL', 'INFO')
        iLevel = getattr(logging, str(level), INFO)
        if isinstance(iLevel, int):
            log.setLevel(iLevel)
            print('Logging level set to', iLevel, level)

    return app

def init_app( app ):
    assert app is not None
    print('Initializing...')
    from . import routes
    return
