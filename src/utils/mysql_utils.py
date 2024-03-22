from datetime import datetime

import mysql.connector
import pytz
from mysql.connector import Error
from dotenv import load_dotenv
import os


def fetch_mysql_connection_details():
    """
    Fetch the environment variables for the MySQL database from the .env file.
    Returns:
        host: The host of the MySQL database
        user: The username of the MySQL database
        passwd: The password of the MySQL database
        database: The name of the MySQL database
    """
    load_dotenv()
    host = os.getenv('MYSQL_HOST')
    user = os.getenv('MYSQL_USERNAME')
    passwd = os.getenv('MYSQL_PASSWORD')
    database = os.getenv('MYSQL_DATABASE')
    return host, user, passwd, database

def create_db_connection():
    """
    Create a connection to the MySQL database.
    Returns:
        The connection to the MySQL database
    """
    host, user, passwd, database = fetch_mysql_connection_details()
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

def get_israel_time():
    """
    Get the current time in Israel.
    Returns:
        The current time in Israel.
    """
    israel_tz = pytz.timezone('Israel')
    now = datetime.now(israel_tz).strftime('%Y-%m-%d %H:%M:%S')
    return now

def get_table_data(table, connection):
    """
    Get all the records from a table in the database.
    Args:
        table: The name of the table
        connection: The connection to the database

    Returns:
         A list of all the records in the table
    """
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    records = cursor.fetchall()
    cursor.close()
    return records