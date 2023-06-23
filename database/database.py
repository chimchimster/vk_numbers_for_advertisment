from dataclasses import dataclass
from decorators import connect_db


@dataclass
class MySQLDatabase:
    _db_name: str

    @connect_db
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


m = MySQLDatabase('temp_db')
m.insert_into_table('phone_numbers', ['first_name', 'last_name', 'date_of_birth', 'phone_number', 'sex', 'sold_status'], [('artem', 'kasyan', '01.01.2000', '+79994344422', '2', '1',)])

