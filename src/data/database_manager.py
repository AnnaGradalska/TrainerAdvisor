import sqlite3
import logging

from PyQt5.QtWidgets import QMessageBox

logging.basicConfig(filename='example.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class DatabaseManager:
    def __init__(self, db_path="src//data//database.db"):
        self.db_path = db_path
        self.conn = None
        self.cur = None
        self.connect_and_initialize()

    def connect_and_initialize(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cur = self.conn.cursor()
            self.create_tables()
        except sqlite3.OperationalError as e:
            logging.exception(e)
            raise
        except Exception as e:
            logging.exception(e)
            raise

    def create_tables(self):
        self.create_tables_trainees()
        self.create_tables_workouts()
        self.create_customized_exercises()
        self.create_personal_records()


        try:
            self.conn.commit()
        except sqlite3.Error as e:
            logging.exception(e)
            raise
        except Exception as e:
            logging.exception(e)
            raise
        #self.conn.close()

    def create_tables_trainees(self):
        self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS trainees (
                    tra_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tra_name TEXT NOT NULL,
                    tra_surname TEXT NOT NULL,
                    tra_email TEXT NOT NULL,
                    tra_date_of_birth DATE NOT NULL,
                    tra_phone TEXT NOT NULL,
                    tra_weight INTEGER NOT NULL,
                    tra_training_start_date DATE NOT NULL
                    )
                ''')

    def create_tables_workouts(self):
        self.cur.execute('''
                        CREATE TABLE IF NOT EXISTS workouts (
                        wor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        wor_tra_id INTEGER NOT NULL,
                        wor_name TEXT NOT NULL,
                        wor_training_start_date DATE NOT NULL,
                        wor_description TEXT,
                        FOREIGN KEY (wor_tra_id) REFERENCES trainee(tra_id) ON DELETE CASCADE
                    )
                ''')

    def create_customized_exercises(self):
        self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS customized_exercises (
                        cus_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cus_name TEXT NOT NULL,
                        cus_wor_id INTEGER NOT NULL,
                        cus_reps INTEGER NOT NULL,
                        cus_sets INTEGER NOT NULL,
                        cus_desc TEXT,
                        FOREIGN KEY (cus_wor_id) REFERENCES workouts(wor_id) ON DELETE CASCADE
                    )
                ''')

    def create_personal_records(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS personal_records (
                per_id INTEGER PRIMARY KEY AUTOINCREMENT,
                per_tra_id INTEGER NOT NULL,
                per_squat REAL NOT NULL,
                per_bench_press REAL NOT NULL,
                per_deadlift REAL NOT NULL,
                per_date DATE NOT NULL,
                FOREIGN KEY (per_tra_id) REFERENCES trainee(tra_id) ON DELETE CASCADE
            )
        ''')

    def close_connection(self):
        """
        Closes the connection to the SQLite database.
        """
        self.conn.close()

    def add_data(self, table_name, values):
        columns = ', '.join(values.keys())
        placeholders = ', '.join('?' * len(values))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            self.cur.execute(query, tuple(values.values()))
            self.conn.commit()
        except sqlite3.Error as e:
            DatabaseManager.show_popup(f"Błąd SQL: {e}")
            return False
        except Exception as e:
            DatabaseManager.show_popup(f"Błąd SQL: {e}")
            return False

        last_row_id = self.cur.lastrowid
        print(last_row_id)
        return last_row_id

    def add_multiple_data(self, table_name, values):
        columns = ', '.join(values[0].keys())
        placeholders = ', '.join('?' * len(values[0]))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        data_values = [tuple(data.values()) for data in values]

        try:
            self.cur.executemany(query, data_values)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            DatabaseManager.show_popup(f"Błąd SQL: {e}")
            return False
        except Exception as e:
            DatabaseManager.show_popup(f"Błąd SQL: {e}")
            return False

    def delete_data(self, table_name, trainee_id):
        query = f"DELETE FROM {table_name} WHERE tra_id = ?"
        self.cur.execute(query, (trainee_id,))
        self.conn.commit()

    def get_data(self, table_name, name_of_field_id, ids):
        if not isinstance(ids, list):
            ids = [ids]

        placeholders = ', '.join('?' * len(ids))

        query = f"SELECT * FROM {table_name} WHERE {name_of_field_id} IN ({placeholders})"
        print(query)
        try:
            self.cur.execute(query, tuple(ids))
            self.conn.commit()
        except sqlite3.Error as e:
            DatabaseManager.show_popup(f"Błąd SQL: {e}")
            return False
        except Exception as e:
            DatabaseManager.show_popup(f"Błąd SQL: {e}")
            return False

        result = self.cur.fetchall()
        return result

    def select_all(self, table_name):
        query = f"SELECT * FROM {table_name}"
        try:
            self.cur.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            DatabaseManager.show_popup(f"Nie można załadować listy podopiecznych! Błąd SQL: {e}")
            return False
        except Exception as e:
            DatabaseManager.show_popup(f"Błąd SQL: {e}")
            return False
        result = self.cur.fetchall()
        return result

    def select_all_for_id(self, field, table_name, criteria_field, value_of_criteria_field):
        query = f"SELECT {field} FROM {table_name} WHERE {criteria_field} = ?"

        try:
            self.cur.execute(query, (value_of_criteria_field,))
            self.conn.commit()
        except sqlite3.Error as e:
            DatabaseManager.show_popup(f"Nie można wykonać polecenia! Błąd SQL: {e}")
            return False
        except Exception as e:
            DatabaseManager.show_popup(f"Błąd SQL: {e}")
            return False
        result = self.cur.fetchall()
        return result

    @staticmethod
    def show_popup(message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()

