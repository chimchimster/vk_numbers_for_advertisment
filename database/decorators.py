import os
from functools import wraps
from mysql.connector import Connect, Error

from dotenv import load_dotenv

load_dotenv()


def connect_db(func) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> callable:

        connection = Connect(
            host=os.environ.get('MYSQL_HOST'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
        )
        print(connection)
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





