import sqlite3
from contextlib import contextmanager
from datetime import datetime
import pytz

DATABASE_FILENAME = 'api_calls.db'

def create_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DATABASE_FILENAME)
    return conn

@contextmanager
def get_cursor():
    """Provide a transactional scope around a series of operations."""
    conn = create_connection()
    cursor = conn.cursor()
    yield cursor
    conn.commit()
    conn.close()

def create_table():
    """Create the API call logs table if it doesn't already exist."""
    with get_cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS api_call_logs (id INTEGER PRIMARY KEY,
                path TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                ip_address TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")

def log_api_call(path, success, ip_address):
    """Log an API call with the timestamp adjusted to Israel time."""
    israel_tz = pytz.timezone('Israel')
    now = datetime.now(israel_tz).strftime('%Y-%m-%d %H:%M:%S')
    with get_cursor() as cursor:
        cursor.execute("""INSERT INTO api_call_logs (path, success, ip_address, timestamp)
                          VALUES (?, ?, ?, ?)""",
                       (path, success, ip_address, now))