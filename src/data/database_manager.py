import sqlite3


class DatabaseManager:
    def __init__(self, db_path="src//data//database.db"):
        """
        Initializes the DatabaseManager object.

        :param db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

        self.create_tables()

    def create_tables(self):
        """
        Creates tables in the SQLite database if they do not exist.
        """
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS trainees (
            tra_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tra_name TEXT NOT NULL,
            tra_surname TEXT NOT NULL,
            tra_email TEXT NOT NULL,
            tra_date_of_birth DATE NOT NULL,
            tra_phone TEXT NOT NULL,
            tra_weight INTEGER NOT NULL,
            tra_training_start_date DATE NOT NULL,
            tra_deadlift INTEGER NOT NULL,
            tra_benchpress INTEGER NOT NULL,
            tra_squat INTEGER NOT NULL
            )
        ''')

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


        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS weight (
                wei_id INTEGER PRIMARY KEY AUTOINCREMENT,
                wei_tra_id INTEGER NOT NULL,
                wei_date DATE NOT NULL,
                wei_weight INTEGER NOT NULL,
                FOREIGN KEY (wei_tra_id) REFERENCES trainee(tra_id) ON DELETE CASCADE
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS personal_records (
                per_id INTEGER PRIMARY KEY AUTOINCREMENT,
                per_tra_id INTEGER NOT NULL,
                per_date DATE NOT NULL,
                per_squat REAL NOT NULL,
                per_bench_press REAL NOT NULL,
                per_deadlift REAL NOT NULL,
                FOREIGN KEY (per_tra_id) REFERENCES trainee(tra_id) ON DELETE CASCADE
            )
        ''')

        self.conn.commit()
        #self.conn.close()

    def close_connection(self):
        """
        Closes the connection to the SQLite database.
        """
        self.conn.close()

    def add_data(self, table_name, values):
        """
        Adds data to the specified table in the SQLite database.

        :param table_name: Name of the table.
        :param values: Dictionary of column names and corresponding values.
        :return: ID of the last inserted row.
        """
        columns = ', '.join(values.keys())
        placeholders = ', '.join('?' * len(values))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        self.cur.execute(query, tuple(values.values()))
        self.conn.commit()

        last_row_id = self.cur.lastrowid
        print(last_row_id)
        return last_row_id

    def add_multiple_data(self, table_name, values):
        columns = ', '.join(values[0].keys())
        placeholders = ', '.join('?' * len(values[0]))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        data_values = [tuple(data.values()) for data in values]
        self.cur.executemany(query, data_values)
        self.conn.commit()

    def delete_data(self, table_name, trainee_id):
        """
        Deletes a record from the trainees table based on the provided trainee ID.

        :param table_name: Name of the table.
        :param trainee_id: ID of the trainee to be deleted.
        """
        query = f"DELETE FROM {table_name} WHERE tra_id = ?"
        self.cur.execute(query, (trainee_id,))
        self.conn.commit()

    def get_data(self, table_name, name_of_field_id, ids):
        """
            Retrieve data from the specified table based on the trainee's identifier.

            :param name_of_field_id:
            :param table_name: Name of the table from which to retrieve data.
            :param ids: List of identifiers to filter the data.
            :return: A list of tuples containing the retrieved data. Each tuple represents a row in the table.
                     Returns an empty list if no data is found.
            """
        placeholders = ', '.join('?' * len(ids))
        query = f"SELECT * FROM {table_name} WHERE {name_of_field_id} IN ({placeholders})"

        self.cur.execute(query, tuple(ids))
        self.conn.commit()

        result = self.cur.fetchall()
        return result

    def select_all(self, table_name):
        query = f"SELECT * FROM {table_name}"
        self.cur.execute(query)
        self.conn.commit()
        result = self.cur.fetchall()
        return result

#idk dlaczego nie działa, select nic nie zwraca
    def select_all_for_id(self, field, table_name, criteria_field, value_of_criteria_field):
        print("in db_manager")
        query = f"SELECT {field} FROM {table_name} WHERE {criteria_field} = ?"
        print(query, (value_of_criteria_field,))
        self.cur.execute(query, (value_of_criteria_field,))
        self.conn.commit()
        result = self.cur.fetchall()
        return result
