# FIXME: license

"""Logging set up."""

import logging
import os
import sys
import traceback

from logging.handlers import RotatingFileHandler

import xdg.BaseDirectory


class CustomRotatingFH(RotatingFileHandler):
    """Rotating handler that starts a new file for every run."""

    def __init__(self, *args, **kwargs):
        RotatingFileHandler.__init__(self, *args, **kwargs)
        self.doRollover()


def exception_handler(exc_type, exc_value, tb):
    """Handle an unhandled exception."""
    exception = traceback.format_exception(exc_type, exc_value, tb)
    msg = "".join(exception)
    print(msg, file=sys.stderr)

    # log
    logger = logging.getLogger('recordium')
    logger.error("Unhandled exception!\n%s", msg)


def set_up(verbose):
    """Set up the logging."""
    logfile = os.path.join(xdg.BaseDirectory.xdg_cache_home, 'recordium', 'recordium.log')
    print("Saving logs to", repr(logfile))
    logfolder = os.path.dirname(logfile)
    if not os.path.exists(logfolder):
        os.makedirs(logfolder)

    logger = logging.getLogger('recordium')
    handler = CustomRotatingFH(logfile, maxBytes=1e6, backupCount=10)
    logger.addHandler(handler)
    formatter = logging.Formatter("%(asctime)s  %(name)-22s  %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)

    if verbose:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # hook the exception handler
    sys.excepthook = exception_handler
