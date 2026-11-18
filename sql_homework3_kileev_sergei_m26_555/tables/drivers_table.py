# Таблица Водители и особые действия с ней

from dbtable import *
from countries_table import CountriesTable

class DriversTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "DRIVERS"

    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"],
                "GIVEN_NAME": ["varchar(64)", "NOT NULL"],
                "SURNAME": ["varchar(64)", "NOT NULL"],
                "BIRTHDAY": ["timestamp", "NOT NULL"],
                "NATIONALITY_CODE": ["varchar(3)", "NOT NULL REFERENCES COUNTRIES(CODE) ON DELETE CASCADE"],
                "WINNINGS": ["smallint", "NOT NULL CHECK (WINNINGS >= 0)"]}

    def primary_key(self):
        return ['id']

    def country_drivers(self, country_full_name):
        countries_table = CountriesTable()
        country_code = countries_table.get_code_from_full_name(country_full_name)
        sql = "SELECT * FROM " + self.table_name() + " WHERE NATIONALITY_CODE = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (country_code,))
        return cur.fetchall()

    def add_driver(self, given_name, surname, birthday, country_full_name, winnings):
        countries_table = CountriesTable()
        nationality_code = countries_table.get_code_from_full_name(country_full_name)
        sql = "INSERT INTO " + self.table_name() + " (GIVEN_NAME, SURNAME, BIRTHDAY, NATIONALITY_CODE, WINNINGS)"
        sql += " VALUES (%s, %s, %s, %s, %s)"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (given_name, surname, birthday, nationality_code, winnings,))
        self.dbconn.conn.commit()
        return True

    def delete_driver(self, given_name, surname):
        sql = "DELETE FROM " + self.table_name() + " WHERE GIVEN_NAME = %s AND SURNAME = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (given_name, surname,))
        self.dbconn.conn.commit()
        return True
