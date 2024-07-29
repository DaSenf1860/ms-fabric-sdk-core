import logging
import os
from warnings import simplefilter

# Initialize logger for msfabricpysdkcore
logger: logging.Logger = logging.getLogger()

_logger = logger.getChild(__name__)

# Ensure warnings are always shown
simplefilter('always', DeprecationWarning)
simplefilter('always', FutureWarning)

# Add a NullHandler by default (https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library)
logger.addHandler(logging.NullHandler())

# Add a handler to log to console if desired (based on FABRIC_SDK_DEBUG environment variable)
if os.environ.get('FABRIC_SDK_DEBUG'):
    logging.captureWarnings(True)
    logging.getLogger("urllib3").setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)
    console_handler: logging.StreamHandler = logging.StreamHandler()
    console_formatter: logging.Formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    _logger.debug("Fabric SDK Debug mode. Logging to console enabled.")

_logger.debug("Logger initialized")

__all__ = ["logger"]