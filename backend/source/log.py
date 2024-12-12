import logging
import os

# Ensure the log directory exists
log_directory = 'log'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up basic configuration with the desired log file path
logging.basicConfig(
    level=logging.DEBUG,
    format='[ %(asctime)s ]  Module: %(filename)s | Function: %(funcName)s | Line No: %(lineno)d -  %(levelname)s: %(message)s',
    filename=os.path.join(log_directory, 'docease.log'),
    filemode='w'  # 'w' for write mode, 'a' for append mode
)

logger = logging.getLogger(__name__)

logger.info("Logging started!")
