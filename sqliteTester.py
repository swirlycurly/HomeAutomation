import sys

from sqliteDatabase import sqliteDatabase


def main():
    db = sqliteDatabase("test.db")
    table_name = "tempData"
    db.create_data_table(table_name)
    db.add_data(table_name, 1.0)
    db.add_data(table_name, 2.0)
    db.add_data(table_name, 3.0)
    db.add_data(table_name, 4.0)
    db.add_data(table_name, 5.0)
    db.add_data(table_name, 6.0)


if __name__ == "__main__":
    main()
