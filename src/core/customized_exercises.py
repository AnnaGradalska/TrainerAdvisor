from src.data.database_manager import DatabaseManager


class CustomizedExercises:
    TABLE_NAME = "customized_exercises"

    def __init__(self, wor_id, name, reps, sets, desc=None):
        """
        Initializes the CustomizedExercises object.

        :param wor_id: Identifier for the workout.
        :param reps: Number of repetitions for the customized exercise.
        :param sets: Number of sets for the customized exercise.
        :param desc: Optional description for the customized exercise.
        """

        self.wor_id = wor_id
        self.name = name
        self.reps = reps
        self.sets = sets
        self.desc = desc
        self.id = None

    def add_customized_exercise_to_db(self, db_manager):
        """
        Adds the customized exercise to the database.

        :param db_manager: DatabaseManager object for handling database operations.
        """
        values = {
            'cus_wor_id': self.wor_id,
            'cus_name': self.name,
            'cus_reps': self.reps,
            'cus_sets': self.sets,
            'cus_desc': self.desc
        }

        self.id = db_manager.add_data(self.TABLE_NAME, values)

    @staticmethod
    def add_multiple_customized_exercises_to_db(db_manager, exercises):
        values_list = []
        for exe in exercises:
            values = {
                'cus_wor_id': exe[0],
                'cus_name': exe[1],
                'cus_reps': exe[2],
                'cus_sets': exe[3],
                'cus_desc': exe[4]
            }
            values_list.append(values)
        db_manager.add_multiple_data(CustomizedExercises.TABLE_NAME, values_list)


    def delete_customized_exercise_from_db(self, db_manager):
        """
        Deletes the customized exercise from the database.

        :param db_manager: DatabaseManager object for handling database operations.
        """
        db_manager.delete_data(self.TABLE_NAME, self.id)

    def get_customized_exercises(self, db_manager):
        """
        Retrieve customized exercises data from the database.

        :param db_manager: DatabaseManager object for handling database operations.
        :return: A list of tuples containing the retrieved customized exercises data.
                 Each tuple represents a row in the 'customized_exercises' table.
                 Returns an empty list if no data is found.
        """
        return db_manager.get_data(self.TABLE_NAME, self.id)

    @staticmethod
    def get_customized_exercises_for_trainee(values, db_manager):
        #db_manager = DatabaseManager()

        return db_manager.get_data(CustomizedExercises.TABLE_NAME, "cus_wor_id", values)
