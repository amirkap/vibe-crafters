from datetime import datetime

import mysql.connector
import pytz
from mysql.connector import Error
from dotenv import load_dotenv
import os

def log_exception_to_db(level, message):
    """
    Log an exception to the database.
    Args:
        level: The level of the exception (e.g. ERROR, WARNING, INFO)
        message: The message of the exception

    Exceptions:
        Error: An error occurred logging the exception to the database
    """
    israel_tz = pytz.timezone('Israel')
    now = datetime.now(israel_tz).strftime('%Y-%m-%d %H:%M:%S')

    load_dotenv()
    host = os.getenv('MYSQL_HOST')
    user = os.getenv('MYSQL_USERNAME')
    passwd = os.getenv('MYSQL_PASSWORD')
    database = os.getenv('MYSQL_DATABASE')
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=passwd
        )
        cursor = connection.cursor()
        query = "INSERT INTO ExceptionLogs (level, message, timestamp) VALUES (%s, %s, %s)"
        cursor.execute(query, (level, message, now))
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
    Exceptions:
        Error: An error occurred getting the exception logs from the database
    """
    load_dotenv()
    host = os.getenv('MYSQL_HOST')
    user = os.getenv('MYSQL_USERNAME')
    passwd = os.getenv('MYSQL_PASSWORD')
    database = os.getenv('MYSQL_DATABASE')
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=passwd
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ExceptionLogs")
        logs = cursor.fetchall()
        cursor.close()
        connection.close()
        return logs
    except Error as e:
        print(f"Error getting exception logs from database: {e}")