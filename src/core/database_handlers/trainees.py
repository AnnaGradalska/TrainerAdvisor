from src.core.database_handlers.personal_records import PersonalRecords
from src.core.database_handlers.workouts import Workouts


class Trainees:
    TABLE_NAME = "trainees"

    def __init__(self, name, surname, email,
                 date_of_birth, phone, training_start_date,
                 weight, id=None):

        self.name = name
        self.surname = surname
        self.email = email
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.training_start_date = training_start_date
        self.weight = weight
        self.id = id

    def add_trainee_to_db(self, db_manager):
        values = {
            'tra_name': self.name,
            'tra_surname': self.surname,
            'tra_email': self.email,
            'tra_date_of_birth': self.date_of_birth,
            'tra_phone': self.phone,
            'tra_weight': self.weight,
            'tra_training_start_date': self.training_start_date,
        }
        result = db_manager.add_data(self.TABLE_NAME, values)
        if not result:
            return False

        self.id = result
        return True

    def delete_trainee_from_db(self, db_manager):
        db_manager.delete_data(self.TABLE_NAME, self.id)

    # def get_trainee_from_db(self, db_manager):
    #     """
    #     Retrieve trainee data from the database.
    #
    #     :param db_manager: DatabaseManager object for handling database operations.
    #     :return: A list of tuples containing the retrieved trainee data.
    #              Each tuple represents a row in the 'trainees' table.
    #              Returns an empty list if no data is found.
    #     """
    #     return db_manager.get_data(self.TABLE_NAME, "tra_id", self.id)

    def select_all(self, db_manager):
        result = db_manager.select_all(Trainees.TABLE_NAME)
        if not result:
            return False
        return result

    # przemyśleć jak tworzyć w inny sposób instację i db_manager
    def select_all_trainings(self, db_manager):
        workout = Workouts("tra_id", "name", "training_start_date", "description=None")
        result = workout.get_workouts_for_trainee_from_db(self.id, db_manager)
        if not result:
            return False
        return result

    def select_all_personal_records(self, db_manager):
        personal_records = PersonalRecords("tra_id", "squat", "bench_press", "deadlift", "date")
        result = personal_records.get_personal_records_for_trainee_from_db(self.id, db_manager)
        if not result:
            return False
        return result
