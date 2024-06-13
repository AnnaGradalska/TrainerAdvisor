from src.data.database_manager import DatabaseManager


class Workouts:
    TABLE_NAME = "workouts"

    def __init__(self, tra_id, name,
                 training_start_date, description=None):
        """
        Initializes the Workouts object.

        :param tra_id: Trainee identifier.
        :param name: Name of the workout.
        :param training_start_date: Date the workout is started.
        :param description: Optional description of the workout.
        """
        self.tra_id = tra_id
        self.name = name
        self.training_start_date = training_start_date
        self.description = description
        self.id = None

    def add_workout_to_db(self, db_manager):
        """
        Adds the workout record to the database.

        :param db_manager: DatabaseManager object for handling database operations.
        """
        values = {
            'wor_tra_id': self.tra_id,
            'wor_name': self.name,
            'wor_training_start_date': self.training_start_date,
            'wor_description': self.description
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

    # def get_workout_from_db(self, db_manager):
    #     """
    #     Retrieve workout data from the database.
    #
    #     :param db_manager: DatabaseManager object for handling database operations.
    #     :return: A list of tuples containing the retrieved workout data.
    #              Each tuple represents a row in the 'workouts' table.
    #              Returns an empty list if no data is found.
    #     """
    #     return db_manager.get_data(self.TABLE_NAME, "wor_id", self.id)

    @staticmethod
    def get_workout_from_db_by_id(db_manager, id):
        result = db_manager.get_data(Workouts.TABLE_NAME, "wor_id", id)

        if not result:
            return False
        return result


    def get_workouts_for_trainee_from_db(self, trainee_id, db_manager):
        result = db_manager.select_all_for_id("wor_id", Workouts.TABLE_NAME, "wor_tra_id", trainee_id)
        if not result:
            return False

        return result

    def select_all(self, db_manager):
        result = db_manager.select_all(self.TABLE_NAME)
        if not result:
            return False
        return result
