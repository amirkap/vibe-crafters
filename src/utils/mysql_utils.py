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


def get_config_value(key_name):
    """
    Get a configuration value from the database.
    Args:
        key_name: The key name of the configuration value

    Returns:
        The value of the configuration
    """
    # Connect to the database
    connection = create_db_connection()
    try:
        cursor = connection.cursor()
        # Fetch the configuration value
        sql = "SELECT value_name FROM ConfigVariables WHERE key_name = %s"
        cursor.execute(sql, (key_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    finally:
        connection.close()

def update_config_value(key_name, value_name):
    """
    Update a configuration value in the database.
    Args:
        key_name: The key name of the configuration value
        value_name: The new value of the configuration
    """
    connection = create_db_connection()
    try:
        cursor = connection.cursor()
        sql = "UPDATE ConfigVariables SET value_name = %s WHERE key_name = %s"
        cursor.execute(sql, (value_name, key_name))
        connection.commit()
    finally:
        connection.close()
