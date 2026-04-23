import logging
import sys


def setup_logging() -> None:
    """
    Configures the logging settings for the application. This function sets up a basic logging configuration that
        outputs log messages to the console with a specific format. The log level is set to INFO, which means that all
        messages at this level and above (WARNING, ERROR, CRITICAL) will be logged. This setup allows for consistent
        and informative logging throughout the application, making it easier to track the flow of execution and diagnose
        issues.
    """
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)  # To output to the terminal console
        ]
    )
