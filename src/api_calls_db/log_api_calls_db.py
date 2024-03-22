import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv, set_key, dotenv_values
from contextlib import contextmanager
from datetime import datetime
import pytz

def create_db_connection():
    """Create a connection to the SQLite database."""
    load_dotenv()
    host = os.getenv('MYSQL_HOST')
    user = os.getenv('MYSQL_USERNAME')
    passwd = os.getenv('MYSQL_PASSWORD')
    database = os.getenv('MYSQL_DATABASE')
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database,
        )
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")

def log_api_call(path, success, ip_address):
    """Log an API call with the timestamp adjusted to Israel time."""
    connection = create_db_connection()
    cursor = connection.cursor()
    israel_tz = pytz.timezone('Israel')
    now = datetime.now(israel_tz).strftime('%Y-%m-%d %H:%M:%S')

    query = """
    INSERT INTO api_call_logs (path, success, ip_address, timestamp)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (path, success, ip_address, now))
    connection.commit()
    cursor.close()
    connection.close()

def get_api_call_logs():
    """Get all the API call logs."""
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM api_call_logs")
    logs = cursor.fetchall()
    cursor.close()
    connection.close()
    return logs

#log_api_call('/api/v1/playlist', True, '1.1.1.1')
print(get_api_call_logs())