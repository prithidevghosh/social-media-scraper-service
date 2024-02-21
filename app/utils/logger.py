import logging
import coloredlogs

# Configure the logger
coloredlogs.install(
    level='DEBUG',  # Set the desired log level
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Create a logger
logger = logging.getLogger('my_logger')

# # Log messages with different log levels
# logger.debug("This is a debug message.")
# logger.info("This is an info message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")
# logger.critical("This is a critical message.")