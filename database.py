import sqlite3
from datetime import datetime


class TimeSeriesDb:
    def __init__(self, db_name):
        self.con = sqlite3.connect(db_name)
        self.db_name = db_name
        self.cols = {}

    def _check_table_name(self, table_name):
        if table_name.isalnum() is False:
            message = f"Table name {table_name} is not an alphanumeric"
            raise Exception(message)

    def create_table(self, table_name, *cols):
        try:
            self._check_table_name(table_name)
            self.cols[table_name] = cols
            col_names = ",".join(cols)
            query = f"""CREATE TABLE IF NOT EXISTS
                   {table_name}(datetime TEXT PRIMARY KEY,
                   {col_names})
                   WITHOUT ROWID"""
            self.con.cursor().execute(query)

            self.con.commit()

        except sqlite3.Error as e:
            print(e)
            self.con.close()

    def add_data(self, table_name, *data):
        try:
            self._check_table_name(table_name)
            self.con.cursor().execute(
                f"""INSERT INTO {table_name}
                (datetime,{",".join(self.cols[table_name])})
               VALUES({",".join(["?"] * (1 + len(data)))})""",
                (datetime.now(), *data),
            )
            self.con.commit()
        except sqlite3.Error as e:
            print(e)
            self.con.close()
