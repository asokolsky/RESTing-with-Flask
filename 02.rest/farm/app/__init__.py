from flask import Flask
import logging
# CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
from logging import getLogger, INFO, Logger
from os.path import abspath, join
from typing import Optional

# main application
app: Optional[Flask] = None
log: Optional[Logger] = None


def create_app(cfgfile: str) -> Flask:
    '''
    Create main app object, while ingesting the settings from the cfgfile
    '''
    global app
    global log
    if app is None:
        static_folder = abspath('static')
        app = Flask(
            # __name__,
            'farm',
            static_folder=static_folder, static_url_path='',
            instance_path=abspath(join(__file__, '../../conf')),
            instance_relative_config=True)
        print('Serving static content from', static_folder, '...')
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


def init_app(app: Flask) -> None:
    assert app is not None
    print('Initializing...')
    from . import routes
    return
