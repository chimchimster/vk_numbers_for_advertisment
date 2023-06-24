import os
from functools import wraps
from clickhouse_driver import Client, errors
from mysql.connector import Connect, Error

from dotenv import load_dotenv

load_dotenv()


def connect_db_mysql(func) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> callable:

        connection = Connect(
            host=os.environ.get('MYSQL_HOST'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
        )

        try:
            result = func(*args, connection=connection, **kwargs)
        except Error as e:
            print(e)
        else:
            connection.commit()
            return result
        finally:
            connection.close()

    return wrapper


def connect_db_clickhouse(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        connection = Client(
            host=os.environ.get('click_host'),
            port=9000,
            user=os.environ.get('click_user'),
            password=os.environ.get('click_password'),
        )

        try:
            result = func(*args, connection=connection, **kwargs)
        except errors as e:
            print(e)
        else:
            return result

    return wrapper



