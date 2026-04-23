import time
import logging


logger = logging.getLogger(__name__)


# ----------------------------------------------
# POC task logic implementation
# ----------------------------------------------

def fetch_data_task() -> str:
    """
    Simulates fetching data from an external source. In a real implementation, this could involve making API calls,
        connecting to databases, or reading from files. The function includes logging statements to indicate the
        progress of the task.
    Returns:
            str: A string indicating the success of the task. In a real implementation, this could return the fetched
            data or a more complex result object.
    """
    logger.info("[Task 1] Fetching data from external source...")
    time.sleep(0.5)
    logger.info("[Task 1] Downloaded records.")
    return "success"


def process_data_task() -> str:
    """
    Simulates processing the fetched data. This could involve cleaning, transforming, or analyzing the data. The
        function includes logging statements to indicate the progress of the task.
    Returns:
        str: A string indicating the success of the task. In a real implementation, this could return the processed data
            or a more complex result object.
    """
    logger.info("[Task 2] Processing data...")
    time.sleep(0.5)
    logger.info("[Task 2] Cleaned records, removed duplicates.")
    return "success"


def store_data_task() -> str:
    """
    Simulates storing the processed data into a database. This could involve inserting records, updating existing data,
        or performing batch operations. The function includes logging statements to indicate the progress of the task.
    Returns:
            str: A string indicating the success of the task. In a real implementation, this could return a status
                message, the number of records inserted, or a more complex result object.
    """
    logger.info("[Task 3] Storing data into database...")
    time.sleep(0.5)
    logger.info("[Task 3] Successfully inserted records.")
    return "success"
