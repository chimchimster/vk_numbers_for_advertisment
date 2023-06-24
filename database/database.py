from dataclasses import dataclass
from .decorators import connect_db_mysql


@dataclass
class MySQLDatabase:
    _db_name: str

    @connect_db_mysql
    def insert_into_table(self, table_name: str, columns: list, collection: list, *args, **kwargs):

        _s = '%s,'*len(columns)

        query = f"insert ignore into {self._db_name}.{table_name} ({','.join(columns)}) values ({_s[:-1]})"

        cursor = self.retrieve_cursor(kwargs)

        match len(collection):
            case 1:
                cursor.execute(query, collection[0])
            case _:
                cursor.executemany(query, collection)

    @staticmethod
    def retrieve_cursor(kwargs):

        connection = kwargs.pop('connection')

        cursor = connection.cursor()

        return cursor