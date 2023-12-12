from src.core.workouts import Workouts


class Trainees:
    TABLE_NAME = "trainees"

    def __init__(self, name, surname, email,
                 date_of_birth, phone, training_start_date,
                 weight, deadlift, benchpress, squat, id = None):
        """
        Initializes the Trainees object.

        :param name: First name of the trainee.
        :param surname: Last name of the trainee.
        :param email: Email address of the trainee.
        :param date_of_birth: Date of birth of the trainee.
        :param phone: Phone number of the trainee.
        :param training_start_date: Date when the training for the trainee started.
        """
        self.name = name
        self.surname = surname
        self.email = email
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.training_start_date = training_start_date
        self.weight = weight
        self.deadlift = deadlift
        self.benchpress = benchpress
        self.squat = squat
        self.id = id

    def add_trainee_to_db(self, db_manager):
        """
        Adds the trainee to the database.

        :param db_manager: DatabaseManager object for handling database operations.
        """
        values = {
            'tra_name': self.name,
            'tra_surname': self.surname,
            'tra_email': self.email,
            'tra_date_of_birth': self.date_of_birth,
            'tra_phone': self.phone,
            'tra_weight': self.weight,
            'tra_training_start_date': self.training_start_date,
            'tra_deadlift': self.deadlift,
            'tra_benchpress': self.benchpress,
            'tra_squat': self.squat
        }

        self.id = db_manager.add_data(self.TABLE_NAME, values)

    def delete_trainee_from_db(self, db_manager):
        """
        Deletes the trainee from the database.

        :param db_manager: DatabaseManager object for handling database operations.
        """
        db_manager.delete_data(self.TABLE_NAME, self.id)

    def get_trainee_from_db(self, db_manager):
        """
        Retrieve trainee data from the database.

        :param db_manager: DatabaseManager object for handling database operations.
        :return: A list of tuples containing the retrieved trainee data.
                 Each tuple represents a row in the 'trainees' table.
                 Returns an empty list if no data is found.
        """
        return db_manager.get_data(self.TABLE_NAME, "tra_id", self.id)

    def select_all(self, db_manager):
        return db_manager.select_all(self.TABLE_NAME)

# przemyśleć jak tworzyć w inny sposób instację i db_manager
    def select_all_trainings(self, db_manager):
        print("in trainnes")
        print(self.id)
        workout = Workouts("tra_id", "name", "training_start_date", "description=None")
        return workout.get_workouts_for_trainee_from_db(self.id)
