import os
import importlib
import sys
import logging
logger = logging.getLogger(__name__)

QUEUE_NAME = 'transform'

environ = os.environ.get('GRIMLOCK')
# Set environment specific settings.
if environ:
    _this_module = sys.modules[__name__]
    try:
        _m = importlib.import_module('config.%s_settings' % environ)
    except ImportError, ex:
        pass
    else:
        print "Using GRIMLOCK=%s" % environ
        for _k in dir(_m):
            setattr(_this_module, _k, getattr(_m, _k))
# Dev is the default environment.
else:
    try:
        from development_settings import *
        logger.info("Using GRIMLOCK=%s" % environ)
    except ImportError, ex:
        pass