from src.core.database_handlers.workouts import Workouts


class PersonalRecords:
    TABLE_NAME = "personal_records"

    def __init__(self, tra_id, squat, bench_press, deadlift, date):
        self.tra_id = tra_id
        self.squat = squat
        self.bench_press = bench_press
        self.deadlift = deadlift
        self.date = date
        self.id = None

    def add_personal_record_to_db(self, db_manager):
        print('w personal records')
        values = {
            'per_tra_id': self.tra_id,
            'per_squat': self.squat,
            'per_bench_press': self.bench_press,
            'per_deadlift': self.deadlift,
            'per_date': self.date,
        }

        result = db_manager.add_data(self.TABLE_NAME, values)
        if not result:
            return False
        self.id = result
        return self.id

    def delete_workout_from_db(self, db_manager):
        """
        Deletes the workout record from the database.

        :param db_manager: DatabaseManager object for handling database operations.
        """
        db_manager.delete_data(self.TABLE_NAME, self.id)

    def get_personal_records_for_trainee_from_db(self, trainee_id, db_manager):
        print("w get_personal records fo trainee")
        result = db_manager.get_data(PersonalRecords.TABLE_NAME, "per_tra_id", trainee_id)
        if not result:
            return False
        print("Rezultat")
        print(result)
        print('po')
        return result
