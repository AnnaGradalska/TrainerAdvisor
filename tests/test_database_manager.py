import unittest
import tempfile
from unittest.mock import patch
from src.data.database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_db_path = f"{self.temp_dir.name}/test.db"

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch('src.data.database_manager.DatabaseManager.show_popup')
    def test_add_data_successful(self, mock_show_popup):
        db_manager = DatabaseManager(db_path="test.db")

        # Przygotowanie danych testowych
        data = {"tra_name": "John", "tra_surname": "Doe", "tra_email": "john.doe@example.com", "tra_date_of_birth": "1990-01-01",
                "tra_phone": "123456789", "tra_weight": 70, "tra_training_start_date": "2022-01-01",
                "tra_deadlift": 150, "tra_benchpress": 100, "tra_squat": 120}


        last_row_id = db_manager.add_data(table_name="trainees", values=data)
        self.assertIsNotNone(last_row_id)

        mock_show_popup.assert_not_called()

        self.assertIsInstance(last_row_id, int)

        retrieved_data = db_manager.get_data(table_name="trainees", name_of_field_id="tra_id", ids=last_row_id)
        self.assertEqual(len(retrieved_data), 1)

        db_manager.close_connection()

if __name__ == '__main__':
    unittest.main()
