import logging
from src.exception_logs_db.log_excetion_to_db import log_exception_to_db


class MySQLLoggingHandler(logging.Handler):
    """
    Custom logging handler to log exceptions to a MySQL database.
    """
    def emit(self, record):
        # Use the log_exception_to_db function to log the record
        log_exception_to_db(record.levelname, self.format(record))

# Create a logger and add the MySQLLoggingHandler
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
mysql_handler = MySQLLoggingHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
mysql_handler.setFormatter(formatter)
logger.addHandler(mysql_handler)