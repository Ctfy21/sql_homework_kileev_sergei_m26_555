import sys
sys.path.append('tables')

from datetime import datetime
import psycopg2

from project_config import *
from dbconnection import *
from dbtable import *
from tables.countries_table import *
from tables.drivers_table import *


class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        self.country_code = None
        self.country_name = None
        return

    def db_error(self):
        self.connection.conn.rollback()
        print("Не удалось обратиться к базе. Если таблицы ещё не созданы, выберите пункт 2.")
        return

    def db_init(self):
        try:
            CountriesTable().create()
            DriversTable().create()
        except psycopg2.Error:
            self.connection.conn.rollback()
            print("Не удалось создать таблицы.")
            return False
        return True

    def db_insert_somethings(self):
        countries = (
            ("GBR", "United Kingdom"),
            ("NLD", "Netherlands"),
            ("MCO", "Monaco"),
        )
        drivers = (
            ("Lewis", "Hamilton", "1985-01-07", "United Kingdom", 105),
            ("Lando", "Norris", "1999-11-13", "United Kingdom", 4),
            ("Max", "Verstappen", "1997-09-30", "Netherlands", 61),
            ("Charles", "Leclerc", "1997-10-16", "Monaco", 8),
        )
        try:
            for code, name in countries:
                CountriesTable().add_country(code, name)
            for given_name, surname, birthday, country_name, winnings in drivers:
                DriversTable().add_driver(given_name, surname, birthday, country_name, winnings)
        except psycopg2.Error:
            self.connection.conn.rollback()
            print("Не удалось заполнить таблицы.")
            return False
        return True

    def db_drop(self):
        try:
            DriversTable().drop()
            CountriesTable().drop()
        except psycopg2.Error:
            self.connection.conn.rollback()
            print("Не удалось удалить таблицы. Сначала удаляются гонщики, потом страны.")
            print("Если на них ссылаются другие таблицы базы, это меню их не трогает.")
            return False
        return True

    def check_country_code(self, code):
        if code is None or code.strip() == "":
            return "Код страны не может быть пустым."
        code = code.strip()
        if len(code) > 3 or any(ch.isspace() for ch in code):
            return "Код страны — от 1 до 3 символов без пробелов."
        return None

    def check_country_name(self, name):
        if name is None or name.strip() == "":
            return "Название страны не может быть пустым."
        if len(name.strip()) > 64:
            return "Название страны не длиннее 64 символов."
        return None

    def check_person_name(self, value, title):
        if value is None or value.strip() == "":
            return title + " не может быть пустым."
        if len(value.strip()) > 64:
            return title + " не длиннее 64 символов."
        return None

    def check_date(self, value):
        if not isinstance(value, str):
            return "Дата рождения должна быть в формате ГГГГ-ММ-ДД."
        try:
            datetime.strptime(value.strip(), "%Y-%m-%d")
        except ValueError:
            return "Дата рождения должна быть в формате ГГГГ-ММ-ДД, например 1997-09-30."
        return None

    def check_winnings(self, value):
        if isinstance(value, bool) or not isinstance(value, int):
            return "Число побед — целое число от 0 до 32767."
        if value < 0 or value > 32767:
            return "Число побед — целое число от 0 до 32767."
        return None

    def read_country_code(self, prompt, allow_empty=False):
        while True:
            raw = input(prompt).strip()
            if raw == "" and allow_empty:
                return ""
            if raw == "" and not allow_empty:
                return None
            message = self.check_country_code(raw)
            if message is not None:
                print(message)
                continue
            return raw

    def read_country_name(self, prompt, allow_empty=False):
        while True:
            raw = input(prompt).strip()
            if raw == "" and allow_empty:
                return ""
            if raw == "" and not allow_empty:
                return None
            message = self.check_country_name(raw)
            if message is not None:
                print(message)
                continue
            return raw

    def read_person_name(self, prompt, title):
        while True:
            raw = input(prompt).strip()
            if raw == "":
                return None
            message = self.check_person_name(raw, title)
            if message is not None:
                print(message)
                continue
            return raw

    def read_date(self, prompt):
        while True:
            raw = input(prompt).strip()
            if raw == "":
                return None
            message = self.check_date(raw)
            if message is not None:
                print(message)
                continue
            return raw

    def read_winnings(self, prompt):
        while True:
            raw = input(prompt).strip()
            if raw == "":
                return None
            if not raw.isdigit():
                print(self.check_winnings(-1))
                continue
            value = int(raw)
            message = self.check_winnings(value)
            if message is not None:
                print(message)
                continue
            return value

    def read_position(self, prompt, count):
        while True:
            raw = input(prompt).strip()
            if raw == "0":
                return None
            if not raw.isdigit():
                print("Нужно ввести номер строки. 0 — отмена.")
                continue
            number = int(raw)
            if number < 1 or number > count:
                print("Нет строки с таким номером.")
                continue
            return number

    def confirm(self, prompt):
        while True:
            answer = input(prompt + " да/нет: ").strip().lower()
            if answer in ("да", "д", "yes", "y"):
                return True
            if answer in ("нет", "н", "no", "n"):
                return False
            print("Введите да или нет.")

    def format_date(self, value):
        if hasattr(value, "strftime"):
            return value.strftime("%Y-%m-%d")
        return str(value)

    def country_rows(self):
        rows = []
        for item in CountriesTable().all_full_names():
            name = item[0]
            code = CountriesTable().get_code_from_full_name(name)
            rows.append((code, name))
        return rows

    def code_exists(self, code):
        for item in CountriesTable().all_codes():
            if item[0] == code:
                return True
        return False

    def print_countries(self, rows):
        print("№\tКод\tНазвание")
        if len(rows) == 0:
            print("Список пуст.")
            return
        for index, row in enumerate(rows, start=1):
            print(str(index) + "\t" + str(row[0]) + "\t" + str(row[1]))
        return

    def print_drivers(self, rows):
        print("№\tИмя\tФамилия\tДата рождения\tПобеды")
        if len(rows) == 0:
            print("У этой страны пока нет гонщиков.")
            return
        for index, row in enumerate(rows, start=1):
            given_name = row[1]
            surname = row[3]
            birthday = self.format_date(row[0])
            winnings = row[4]
            print(str(index) + "\t" + str(given_name) + "\t" + str(surname) + "\t" + birthday + "\t" + str(winnings))
        return

    def show_main_menu(self):
        menu = """Добро пожаловать!
Основное меню (выберите цифру в соответствии с необходимым действием):
    1 - просмотр стран;
    2 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            if self.db_drop() and self.db_init() and self.db_insert_somethings():
                print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step

    def show_countries(self):
        try:
            rows = self.country_rows()
        except psycopg2.Error:
            self.db_error()
            return False
        print("Просмотр списка стран")
        self.print_countries(rows)
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    3 - добавление страны;
    4 - удаление страны;
    5 - изменение страны;
    6 - просмотр гонщиков страны;
    9 - выход."""
        print(menu)
        return True

    def after_show_countries(self, next_step):
        if next_step in ("0", "3", "4", "5", "6", "9"):
            return next_step
        print("Выбрано неверное число! Повторите ввод!")
        return "1"

    def show_add_country(self):
        try:
            while True:
                code = self.read_country_code("Введите код страны, от 1 до 3 символов без пробелов (пустая строка — отмена): ")
                if code is None:
                    print("Добавление отменено.")
                    return
                if self.code_exists(code):
                    print("Страна с таким кодом уже есть. Введите другой код.")
                    continue
                break
            name = self.read_country_name("Введите название страны, не длиннее 64 символов (пустая строка — отмена): ")
            if name is None:
                print("Добавление отменено.")
                return
            CountriesTable().add_country(code, name)
            print("Страна добавлена.")
        except psycopg2.Error:
            self.db_error()
        return

    def show_delete_country(self):
        try:
            rows = self.country_rows()
            if len(rows) == 0:
                print("Список стран пуст.")
                return
            self.print_countries(rows)
            number = self.read_position("Укажите номер строки страны, которую нужно удалить (0 - отмена): ", len(rows))
            if number is None:
                print("Удаление отменено.")
                return
            code = rows[number - 1][0]
            name = rows[number - 1][1]
            linked = DriversTable().country_drivers(name)
            if linked:
                question = "У страны " + name + " есть гонщики: " + str(len(linked)) + ". Они будут удалены вместе со страной. Удалить страну?"
            else:
                question = "Удалить страну " + name + " (" + code + ")?"
            if not self.confirm(question):
                print("Удаление отменено.")
                return
            for driver in linked:
                DriversTable().delete_driver(driver[1], driver[3])
            CountriesTable().delete_country(code)
            print("Страна удалена.")
            if linked:
                print("Гонщики этой страны тоже удалены.")
            if self.country_code == code:
                self.country_code = None
                self.country_name = None
        except psycopg2.Error:
            self.db_error()
        return

    def show_edit_country(self):
        try:
            rows = self.country_rows()
            if len(rows) == 0:
                print("Список стран пуст.")
                return
            self.print_countries(rows)
            number = self.read_position("Укажите номер строки страны, которую нужно изменить (0 - отмена): ", len(rows))
            if number is None:
                print("Изменение отменено.")
                return
            code = rows[number - 1][0]
            old_name = rows[number - 1][1]
            print("Код страны: " + str(code))
            print("Текущее название: " + str(old_name))
            new_name = self.read_country_name("Новое название, не длиннее 64 символов (пустая строка — отмена): ")
            if new_name is None:
                print("Изменение отменено.")
                return
            if new_name == old_name:
                print("Данные не изменились.")
                return
            CountriesTable().update_country(code, new_name)
            print("Страна изменена.")
            if self.country_code == code:
                self.country_name = new_name
        except psycopg2.Error:
            self.db_error()
        return

    def select_country(self):
        try:
            rows = self.country_rows()
        except psycopg2.Error:
            self.db_error()
            return False
        if len(rows) == 0:
            print("Список стран пуст.")
            return False
        print("Выберите страну, гонщиков которой нужно показать.")
        self.print_countries(rows)
        number = self.read_position("Укажите номер строки (0 - отмена): ", len(rows))
        if number is None:
            return False
        self.country_code = rows[number - 1][0]
        self.country_name = rows[number - 1][1]
        return True

    def show_drivers(self):
        try:
            rows = DriversTable().country_drivers(self.country_name)
        except TypeError:
            print("Выбранной страны уже нет.")
            self.country_code = None
            self.country_name = None
            return False
        except psycopg2.Error:
            self.db_error()
            return False
        print("Гонщики страны: " + str(self.country_name))
        self.print_drivers(rows)
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат к списку стран;
    7 - добавление гонщика;
    8 - удаление гонщика;
    9 - выход."""
        print(menu)
        return True

    def after_show_drivers(self, next_step):
        if next_step in ("0", "1"):
            self.country_code = None
            self.country_name = None
            return next_step
        if next_step in ("7", "8", "9"):
            return next_step
        print("Выбрано неверное число! Повторите ввод!")
        return "6"

    def show_add_driver(self):
        if self.country_name is None:
            print("Сначала выберите страну.")
            return
        print("Новый гонщик, страна: " + str(self.country_name))
        try:
            if CountriesTable().get_code_from_full_name(self.country_name) is None:
                print("Выбранной страны уже нет.")
                self.country_code = None
                self.country_name = None
                return
        except TypeError:
            print("Выбранной страны уже нет.")
            self.country_code = None
            self.country_name = None
            return
        except psycopg2.Error:
            self.db_error()
            return
        given_name = self.read_person_name("Имя, не длиннее 64 символов (пустая строка — отмена): ", "Имя")
        if given_name is None:
            print("Добавление отменено.")
            return
        surname = self.read_person_name("Фамилия, не длиннее 64 символов (пустая строка — отмена): ", "Фамилия")
        if surname is None:
            print("Добавление отменено.")
            return
        birthday = self.read_date("Дата рождения в формате ГГГГ-ММ-ДД (пустая строка — отмена): ")
        if birthday is None:
            print("Добавление отменено.")
            return
        winnings = self.read_winnings("Число побед — целое от 0 до 32767 (пустая строка — отмена): ")
        if winnings is None:
            print("Добавление отменено.")
            return
        try:
            DriversTable().add_driver(given_name, surname, birthday, self.country_name, winnings)
            print("Гонщик добавлен.")
        except psycopg2.Error:
            self.db_error()
        return

    def show_delete_driver(self):
        if self.country_name is None:
            print("Сначала выберите страну.")
            return
        try:
            rows = DriversTable().country_drivers(self.country_name)
            if len(rows) == 0:
                print("У этой страны нет гонщиков.")
                return
            self.print_drivers(rows)
            number = self.read_position("Укажите номер строки гонщика, которого нужно удалить (0 - отмена): ", len(rows))
            if number is None:
                print("Удаление отменено.")
                return
            driver = rows[number - 1]
            given_name = str(driver[1])
            surname = str(driver[3])
            same = 0
            for item in rows:
                if str(item[1]) == given_name and str(item[3]) == surname:
                    same += 1
            if same > 1:
                question = "С именем " + given_name + " " + surname + " несколько записей (" + str(same) + "). Удалятся все они. Продолжить?"
            else:
                question = "Удалить гонщика " + given_name + " " + surname + ", дата рождения " + self.format_date(driver[0]) + "?"
            if not self.confirm(question):
                print("Удаление отменено.")
                return
            DriversTable().delete_driver(given_name, surname)
            print("Гонщик удалён.")
        except TypeError:
            print("Выбранной страны уже нет.")
            self.country_code = None
            self.country_name = None
        except psycopg2.Error:
            self.db_error()
        return

    def main_cycle(self):
        current_menu = "0"
        while current_menu != "9":
            if current_menu == "0":
                self.show_main_menu()
                current_menu = self.after_main_menu(self.read_next_step())
            elif current_menu == "1":
                if not self.show_countries():
                    current_menu = "0"
                    continue
                current_menu = self.after_show_countries(self.read_next_step())
            elif current_menu == "3":
                self.show_add_country()
                current_menu = "1"
            elif current_menu == "4":
                self.show_delete_country()
                current_menu = "1"
            elif current_menu == "5":
                self.show_edit_country()
                current_menu = "1"
            elif current_menu == "6":
                if self.country_name is None and not self.select_country():
                    current_menu = "1"
                    continue
                if not self.show_drivers():
                    current_menu = "1"
                    continue
                current_menu = self.after_show_drivers(self.read_next_step())
            elif current_menu == "7":
                self.show_add_driver()
                current_menu = "6"
            elif current_menu == "8":
                self.show_delete_driver()
                current_menu = "6"
        print("До свидания!")
        return

    def test(self):
        DbTable.dbconn.test()

if __name__ == "__main__":
    m = Main()
    # Откоментируйте эту строку и закоментируйте следующую для теста
    # соединения с БД
    # m.test()
    m.main_cycle()
