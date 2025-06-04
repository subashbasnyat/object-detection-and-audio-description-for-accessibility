import logging  
import os       

def setup_logger(name, log_file):
    """
    Create and configure a logger to write logs to a specified file.

    Args:
        name (str): Name of the logger instance.
        log_file (str): Path to the log file where logs will be saved.

    Returns:
        logger (Logger): Configured logger object.
    """

    # Ensure the directory for the log file exists; create it if it doesn't
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Create a logger instance with the specified name
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Set the logging level to INFO

    # Create a file handler to write log messages to the given file
    file_handler = logging.FileHandler(log_file)

    # Define the format for log messages (timestamp | log level | message)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    # Attach the formatter to the file handler
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger instance
    logger.addHandler(file_handler)

    # Return the configured logger to be used elsewhere in the project
    return logger
