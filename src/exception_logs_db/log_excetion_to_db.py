from datetime import datetime

import mysql.connector
import pytz
from mysql.connector import Error
from dotenv import load_dotenv
import os

def log_exception_to_db(level, message):
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

log_exception_to_db('ERROR', 'This is an error message')
