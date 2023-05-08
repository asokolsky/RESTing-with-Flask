import logging
from logging import INFO

log = None


def create_log(app):
    '''
    Setup app logging
    '''
    app.logger.info('Starting farm service...')
    mfmt = "%(asctime)s.%(msecs)03d [%(levelno)s] [%(thread)d] %(filename)s:%(lineno)s %(message)s"
    logging.basicConfig(format=mfmt, datefmt="%Y%m%d.%H%M%S")

    # this logger will be created only when the first message is logged

    # wlog.disabled = True

    global log
    # log = getLogger()
    log = app.logger
    print('Using:', str(log))

    level = app.config.get('LOGGING_LEVEL', 'INFO')
    iLevel = getattr(logging, str(level), INFO)
    if isinstance(iLevel, int):
        log.setLevel(iLevel)
        print('Logging level set to', iLevel, level)

    loggers = [
        logging.getLogger(name) for name in logging.root.manager.loggerDict]
    print('Loggers:', str(loggers))
    return log
