import sqlite3
import os
from sqlite3 import Error


class LocalDB():
    def __init__(self):
        db_route = f"{os.path.dirname(os.path.realpath(__file__))}/lotalf.db"
        self.connection = self.create_connection(db_route)

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn

    def get_all_regions(self):
        cur = self.connection.cursor()
        cur.execute("SELECT DISTINCT(region) FROM towns")

        rows = cur.fetchall()
        row_list = []
        for row in rows:
            row_list.append(row[0])

        return sorted(row_list)

    def get_all_provinces(self, region=None):
        cur = self.connection.cursor()
        if region is None:
            cur.execute("SELECT DISTINCT(province) FROM towns")
        else:
            print(f"SELECT DISTINCT(province) FROM towns WHERE region = '{region}'")
            cur.execute(f"SELECT DISTINCT(province) FROM towns WHERE region = '{region}'")

        rows = cur.fetchall()
        row_list = []
        for row in rows:
            row_list.append(row[0])

        return sorted(row_list)

    def get_all_towns(self, province=None):
        cur = self.connection.cursor()
        if province is None:
            cur.execute("SELECT DISTINCT(town) FROM towns")
        else:
            cur.execute(f"SELECT DISTINCT(town) FROM towns WHERE province = '{province}'")

        rows = cur.fetchall()
        row_list = []
        for row in rows:
            row_list.append(row[0])

        return sorted(row_list)

    def get_all_retailers(self):
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM lottery_retailers WHERE retailer_latitude != '' AND retailer_number != ''")

        rows = cur.fetchall()

        return sorted(rows)

    def get_retailers_count(self):
        cur = self.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM lottery_retailers WHERE retailer_latitude != '' AND retailer_number != ''")

        rows = cur.fetchall()

        return sorted(rows)

    def get_retailers(self, fields, values):
        cur = self.connection.cursor()
        query = "SELECT * FROM lottery_retailers WHERE retailer_latitude != '' AND retailer_number != ''"
        for index in range(0, len(fields)):
            query += f" AND {fields[index]} = '{values[index]}'"
        cur.execute(query)

        rows = cur.fetchall()

        return sorted(rows)

    def get_retailers_like(self, fields, values):
        cur = self.connection.cursor()
        query = "SELECT * FROM lottery_retailers WHERE retailer_latitude != '' AND retailer_number != ''"
        for index in range(0, len(fields)):
            query += f" AND {fields[index]} LIKE '%{values[index]}%'"
        cur.execute(query)

        rows = cur.fetchall()

        return sorted(rows)
