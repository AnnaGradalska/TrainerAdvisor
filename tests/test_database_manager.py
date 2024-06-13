import unittest
import os
import tempfile
import shutil

from PyQt5.QtWidgets import QApplication

from src.data.database_manager import DatabaseManager

app = QApplication([])  # Inicjalizacja aplikacji PyQt

class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.test_dir, 'test_database.db')
        self.db_manager = DatabaseManager(db_path=self.test_db_path)

    def tearDown(self):
        self.db_manager.close_connection()
        shutil.rmtree(self.test_dir)

    def test_connect_and_initialize(self):
        self.assertIsNotNone(self.db_manager.conn)
        self.assertIsNotNone(self.db_manager.cur)


    def test_add_data(self):
        data = {'tra_name': 'John', 'tra_surname': 'Doe', 'tra_email': 'john.doe@example.com',
                'tra_date_of_birth': '2000-01-01', 'tra_phone': '123456789', 'tra_weight': 70,
                'tra_training_start_date': '2022-01-01'}
        last_row_id = self.db_manager.add_data('trainees', data)
        self.assertIsNotNone(last_row_id)

    def test_get_data(self):
        trainee_data = {'tra_name': 'Alice', 'tra_surname': 'Smith', 'tra_email': 'alice.smith@example.com',
                        'tra_date_of_birth': '1995-05-15', 'tra_phone': '987654321', 'tra_weight': 60,
                        'tra_training_start_date': '2021-01-01'}
        trainee_id = self.db_manager.add_data('trainees', trainee_data)

        retrieved_data = self.db_manager.get_data('trainees', 'tra_id', trainee_id)
        self.assertEqual(len(retrieved_data), 1)
        self.assertEqual(retrieved_data[0][1], 'Alice')

    def test_delete_data(self):
        trainee_data = {'tra_name': 'Bob', 'tra_surname': 'Johnson', 'tra_email': 'bob.johnson@example.com',
                        'tra_date_of_birth': '1990-10-10', 'tra_phone': '555555555', 'tra_weight': 75,
                        'tra_training_start_date': '2020-01-01'}
        trainee_id = self.db_manager.add_data('trainees', trainee_data)

        self.db_manager.delete_data('trainees', trainee_id)
        retrieved_data = self.db_manager.get_data('trainees', 'tra_id', trainee_id)
        self.assertEqual(len(retrieved_data), 0)

    def test_select_all(self):
        trainees_data = [
            {'tra_name': 'Tom', 'tra_surname': 'Taylor', 'tra_email': 'tom.taylor@example.com',
             'tra_date_of_birth': '1985-08-20', 'tra_phone': '123123123', 'tra_weight': 80,
             'tra_training_start_date': '2019-01-01'},
            {'tra_name': 'Anna', 'tra_surname': 'Adams', 'tra_email': 'anna.adams@example.com',
             'tra_date_of_birth': '1998-03-25', 'tra_phone': '987987987', 'tra_weight': 55,
             'tra_training_start_date': '2018-01-01'}
        ]
        self.db_manager.add_multiple_data('trainees', trainees_data)

        all_trainees = self.db_manager.select_all('trainees')
        self.assertEqual(len(all_trainees), 2)

if __name__ == '__main__':
    unittest.main()
