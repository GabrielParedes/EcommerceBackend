import MySQLdb
import os


def get_db_connection():
    connection = MySQLdb.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        db=os.getenv("DB_NAME", "ecommerce"),
    )
    return connection


def fetch_all(query):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def is_db_connected():
    try:
        connection = get_db_connection()
        connection.ping()
        connection.close()
        return True
    except MySQLdb.Error:
        return False
