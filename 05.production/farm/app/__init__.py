# For relative imports to work in Python 3.6
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import logging
from logging import (
    getLogger, 
    #CRITICAL, 
    #ERROR, 
    #WARNING, 
    INFO, 
    #DEBUG, 
    #NOTSET
)
from os.path import abspath, join
from flask import Flask

from .metrics import setup_metrics

__version__='2019.11.23'

# main application
app = Flask(
    'farm', #__name__,
    static_folder=abspath(join( __file__, '../../static' )),
    static_url_path='',
    instance_path=abspath(join( __file__, '../../conf' )),
    instance_relative_config=True)
setup_metrics(app)

print('__init__.py: app created')

mfmt = "%(asctime)s.%(msecs)03d [%(levelno)s] [%(thread)d] %(filename)s:%(lineno)s %(message)s"
logging.basicConfig(format=mfmt, datefmt="%Y%m%d.%H%M%S")
log = getLogger()


def init_app(cfgfile):
    assert cfgfile
    global app
    assert app is not None
    global log
    assert log is not None

    print('Loading config from', abspath(cfgfile), '...')
    app.config.from_pyfile(cfgfile)
    level = app.config.get('LOGGING_LEVEL', 'INFO')
    iLevel = getattr(logging, str(level), INFO)
    if isinstance(iLevel, int):
        log.setLevel(iLevel)
        print('Logging level set to', iLevel, level)

    print('Initializing...')
    from . import routes
    from . import dataset

    if not dataset.init_dataset(app.config):
        print('Dataset initialization failed')

    return app
