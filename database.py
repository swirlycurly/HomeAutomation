import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name):
        self.con = sqlite3.connect(db_name)
        self.db_name = db_name

    def _check_table_name(self, table_name):
        if table_name.isalnum() is False:
            message = f"Table name {table_name} is not an alphanumeric"
            raise Exception(message)

    def create_data_table(self, table_name):
        try:
            self._check_table_name(table_name)
            self.con.cursor().execute(
                f"""CREATE TABLE IF NOT EXISTS
                   {table_name}(datetime TEXT PRIMARY KEY, value REAL)
                   WITHOUT ROWID""",
            )

            self.con.commit()

        except sqlite3.Error as e:
            print(e)
            self.con.close()

    def add_data(self, table_name, data):
        try:
            self._check_table_name(table_name)
            self.con.cursor().execute(
                f"""INSERT INTO {table_name}(datetime,value)
                                    VALUES(?,?)""",
                (datetime.now(), data),
            )
            self.con.commit()
        except sqlite3.Error as e:
            print(e)
            self.con.close()
