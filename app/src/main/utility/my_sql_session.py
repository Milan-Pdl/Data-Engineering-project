import mysql.connector
from src.main.utility.logging_config import logger
def get_mysql_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="db_name"
    )
    return connection


