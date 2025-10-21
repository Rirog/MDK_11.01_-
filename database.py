import pymysql as mysql
from peewee import MySQLDatabase
from pymysql import MySQLError


DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "mysql"
DB_NAME = "BazaDannih"


def create_database():
    """Создания базы данных"""
    try:
        conn_mysql = mysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        with conn_mysql.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print(f"База данных '{DB_NAME}' успешна создана")
    except MySQLError as error:
        print(f"Ошибка создания базы данных: {error}")
    finally:
        if 'connection' in locals() and conn_mysql:
            conn_mysql.close()

create_database()

database_connection = MySQLDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
)