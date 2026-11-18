# Таблица Страны и особые действия с ней.

from dbtable import *

class CountriesTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "COUNTRIES"

    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"],
                "CODE": ["varchar(3)", "NOT NULL UNIQUE"],
                "FULL_NAME": ["varchar(64)", "NOT NULL"]}   

    def primary_key(self):
        return ['id']

    def all_codes(self):
        sql = "SELECT CODE FROM " + self.table_name()
        sql += " ORDER BY CODE"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()   

    def get_code_from_full_name(self, full_name):
        sql = "SELECT CODE FROM " + self.table_name() + " WHERE FULL_NAME = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (full_name,))
        return cur.fetchone()[0]

    def all_full_names(self):
        sql = "SELECT FULL_NAME FROM " + self.table_name()
        sql += " ORDER BY FULL_NAME"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()         

    def add_country(self, code, full_name):
        sql = "INSERT INTO " + self.table_name() + " (CODE, FULL_NAME)"
        sql += " VALUES (%s, %s)"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (code, full_name,))
        self.dbconn.conn.commit()
        return True

    def delete_country(self, code):
        sql = "DELETE FROM " + self.table_name() + " WHERE CODE = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (code,))
        self.dbconn.conn.commit()
        return True

    def update_country(self, code, full_name):
        sql = "UPDATE " + self.table_name() + " SET FULL_NAME = %s WHERE CODE = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (full_name, code,))
        self.dbconn.conn.commit()
        return True
