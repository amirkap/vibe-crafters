from src.utils.mysql_utils import *


def log_api_call(path, success, ip_address):
    """
    Log an API call to the database.
    Args:
        path: The path of the API call
        success: Whether the API call was successful
        ip_address: The IP address of the client making the API call
    """
    connection = create_db_connection()
    cursor = connection.cursor()
    current_israel_time = get_israel_time()
    query = """
    INSERT INTO api_call_logs (path, success, ip_address, timestamp)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (path, success, ip_address, current_israel_time))
    connection.commit()
    cursor.close()
    connection.close()

def get_api_call_logs():
    """
    Get all the API call logs from the database.
    Returns:
        A list of all the API call logs
    """
    api_call_logs = get_table_data('api_call_logs', create_db_connection())
    return api_call_logs

def print_api_call_logs():
    """
    Print all the API call logs.
    """
    api_call_logs = get_api_call_logs()
    for log in api_call_logs:
        print(log)