import logging
import os

from pythonjsonlogger import jsonlogger


# Defining a logger which has a file handler (to write to files) and console handler (to write to the terminal)
# the formatter formats the log output to json

def configure_logging():
    # Create logger
    webapp_logger = logging.getLogger(__name__)
    webapp_logger.setLevel(logging.INFO)

    # Configure JSON formatter
    formatter = jsonlogger.JsonFormatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')

    # Configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    webapp_logger.addHandler(console_handler)

    hostname = os.uname().nodename

    # Application during run time checks if it's running on local machine or on a vm
    # (ONLY WORKS IF HOSTNAME RESOLVES to <XYZ>.local for example in my case Siddharths-MacBook-Air.local

    if os.getenv('GITHUB_ACTIONS') == 'true' or hostname.endswith('.local'):
        log_file_path = 'myapp_local.log'
    else:
        log_file_path = '/var/log/webapp/webapp.log'

    # Configure file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    webapp_logger.addHandler(file_handler)

    return webapp_logger


webapp_logger = configure_logging()