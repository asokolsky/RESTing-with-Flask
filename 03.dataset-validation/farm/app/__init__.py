# For relative imports to work in Python 3.6
from flask import Flask
import logging
# getLogger, CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
from logging import Logger, INFO
import os
from os.path import abspath, join
import sys
from typing import Optional

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

    return app


def init_app(app: Flask) -> None:
    assert app is not None
    print('Initializing...')
    global log
    if log is None:
        #
        # what a mess: https://github.com/pallets/flask/issues/2998
        # more in-depth:
        # https://www.scalyr.com/blog/getting-started-quickly-with-flask-logging/
        #
        app.logger.info('Starting farm service...')
        mfmt = "%(asctime)s.%(msecs)03d [%(levelno)s] [%(thread)d] %(filename)s:%(lineno)s %(message)s"
        logging.basicConfig(format=mfmt, datefmt="%Y%m%d.%H%M%S")

        # this logger will be created only when the first message is logged
        # wlog = logging.getLogger("werkzeug")
        # wlog.disabled = True

        # log = getLogger()
        log = app.logger
        print('Using:', str(log))

        level = app.config.get('LOGGING_LEVEL', 'INFO')
        iLevel = getattr(logging, str(level), INFO)
        if isinstance(iLevel, int):
            log.setLevel(iLevel)
            print('Logging level set to', iLevel, level)

        loggers = [logging.getLogger(name) for name in
                   logging.root.manager.loggerDict]
        print('Loggers:', str(loggers))

    from . import routes
    return
