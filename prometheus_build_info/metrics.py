from prometheus_client import Gauge
from json import load
import os
import sys
import logging
from .builder import PROM_BUILD_FILE

logger = logging.getLogger(__name__)

try:
    with open(os.getcwd() + "/" + PROM_BUILD_FILE, "r") as buildinfo:
        info = load(buildinfo)

    metric = info['appname'] + "_build_info"
    build_info = Gauge(metric, 'Build Information',
                       ['branch', 'pythonversion', 'revision', 'version'], multiprocess_mode='max')

    # Extract runtime python version
    python_version_info = sys.version_info
    python_version = "{}.{}.{}".format(python_version_info.major, python_version_info.minor, python_version_info.micro)

    build_info.labels(info['branch'], python_version, info['revision'], info['version']).set(1)
except OSError as err:
    logger.exception("No " + PROM_BUILD_FILE + " file, no metric added")