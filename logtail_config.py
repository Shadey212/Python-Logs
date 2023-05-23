import logging
import os
from logtail import LogtailLogger

# Create a logger
logger = logging.getLogger()

# Retrieve the Logtail source token from an environment variable
source_token = os.getenv('LOGTAIL_SOURCE_TOKEN')

# Create a LogtailLogger instance with the source token
logtail_logger = LogtailLogger(source_token)

# Set the log level for the logger
logger.setLevel(logging.INFO)

# Add the LogtailLogger instance to the logger
logger.addHandler(logtail_logger)