import mysql.connector
from src.main.utility.logging_config import logger
def get_mysql_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="milan@123",
        database="de_project"
    )
    return connection


