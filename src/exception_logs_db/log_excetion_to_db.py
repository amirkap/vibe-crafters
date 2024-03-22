from src.utils.mysql_utils import *

def log_exception_to_db(level, message):
    """
    Log an exception to the database.
    Args:
        level: The level of the exception (e.g. ERROR, WARNING, INFO)
        message: The message of the exception
    """
    connection = create_db_connection()
    current_time = get_israel_time()
    try:
        cursor = connection.cursor()
        query = "INSERT INTO ExceptionLogs (level, message, timestamp) VALUES (%s, %s, %s)"
        cursor.execute(query, (level, message, current_time))
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error logging exception to database: {e}")

def get_exception_logs():
    """
    Get all the exception logs from the database.
    Returns:
        A list of all the exception logs
    """
    exception_logs = get_table_data('ExceptionLogs', create_db_connection())
    return exception_logs

def print_exception_logs():
    """
    Print all the exception logs.
    """
    exception_logs = get_exception_logs()
    for log in exception_logs:
        print(log)
